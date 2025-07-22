# infrastructure/main.tf
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

# Configure the Azure provider
provider "azurerm" {
  features {}
}

# Create resource group for Terraform state (must exist before backend config)
resource "azurerm_resource_group" "tfstate" {
  name     = "tfstate-rg"
  location = "East US" # Change to your preferred region
}

# Create storage account for Terraform state
resource "azurerm_storage_account" "tfstate" {
  name                     = "mediatfstate${substr(md5(azurerm_resource_group.tfstate.id), 0, 8)}" # Unique name
  resource_group_name      = azurerm_resource_group.tfstate.name
  location                = azurerm_resource_group.tfstate.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "terraform"
  }
}

# Create container for Terraform state
resource "azurerm_storage_container" "tfstate" {
  name                  = "tfstate"
  storage_account_name  = azurerm_storage_account.tfstate.name
  container_access_type = "private"
}

# Now configure the backend using the just-created resources
terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "mediatfstate" # This will be replaced with the actual name after first apply
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
    use_azuread_auth     = true  # Add this line
    subscription_id      = "32cac44c-6e25-4b5c-8bb7-d8782197489b"
    tenant_id            = "b1b5c504-6f69-4e15-9c40-ddea95f2b70b"
  }
}

# Main resource group for your application
resource "azurerm_resource_group" "main" {
  name     = "media-assistant-rg"
  location = "East US" # Must match the location above
}

module "networking" {
  source              = "./modules/networking"
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  environment        = "prod"
}

module "database" {
  source              = "./modules/database"
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
}

module "kubernetes" {
  source              = "./modules/kubernetes"
  cluster_name       = "media-assistant-aks"
  location           = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name  # This should be in the module's variables.tf
  #client_id          = var.client_id
  #client_secret      = var.client_secret
  node_count         = 2
}
# App Service Plan for Functions
resource "azurerm_app_service_plan" "backend" {
  name                = "media-assistant-func-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true  # Required for Linux Function Apps

  sku {
    tier = "Basic"
    size = "B1
  }
}

# Storage Account for Functions
resource "azurerm_storage_account" "backend" {
  name                     = "mediafuncstore${random_string.suffix.result}"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# Random suffix for unique names
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# Cosmos DB Account (if missing)
resource "azurerm_cosmosdb_account" "main" {
  name                = "media-assistant-cosmos"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }
}

# Cognitive Services for Speech
resource "azurerm_cognitive_account" "speech" {
  name                = "media-assistant-speech"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "SpeechServices"
  sku_name            = "S0"
}
# Frontend Static Site
  resource "azurerm_static_site" "frontend" {
  name                = "media-assistant-frontend"
  resource_group_name = azurerm_resource_group.main.name
  location           = "EastUS"
}

resource "azurerm_function_app" "backend" {
  name                       = "media-assistant-api"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  app_service_plan_id        = azurerm_app_service_plan.backend.id
  storage_account_name       = azurerm_storage_account.backend.name
  storage_account_access_key = azurerm_storage_account.backend.primary_access_key
  os_type                    = "linux"
  version                    = "~4"

  app_settings = {
    "COSMOS_DB_CONNECTION_STRING" = azurerm_cosmosdb_account.main.connection_strings[0]
    "SPEECH_KEY"                 = azurerm_cognitive_account.speech.primary_access_key
  }
}
