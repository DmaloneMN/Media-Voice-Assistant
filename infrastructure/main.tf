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
# Frontend Static Site
  resource "azurerm_static_site" "frontend" {
  name                = "media-assistant-frontend"
  resource_group_name = azurerm_resource_group.main.name
  location           = "EastUS"
}

# Backend Function App
  resource "azurerm_function_app" "backend" {
  name                       = "media-assistant-api"
  resource_group_name        = azurerm_resource_group.main.name
  location                   = azurerm_resource_group.main.location
  app_service_plan_id        = azurerm_app_service_plan.backend.id
  storage_account_name       = azurerm_storage_account.backend.name
  storage_account_access_key = azurerm_storage_account.backend.primary_access_key
  os_type                    = "linux"
  version                    = "~4"
}
