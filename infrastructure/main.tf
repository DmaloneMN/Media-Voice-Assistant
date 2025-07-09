terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  backend "azurerm" {
    resource_group_name  = "tfstate-rg"
    storage_account_name = "mediatfstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "main" {
  name     = "media-assistant-rg"
  location = "East US"
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
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  client_id           = var.client_id
  client_secret       = var.client_secret
}
