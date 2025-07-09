resource "azurerm_app_service" "frontend" {
  name                = "media-assistant-frontend"
  location            = var.location
  resource_group_name = var.resource_group_name
  app_service_plan_id = azurerm_app_service_plan.frontend.id

  site_config {
    linux_fx_version = "DOCKER|mediaassistant.azurecr.io/frontend:latest"
    always_on        = true
  }

  identity {
    type = "SystemAssigned"
  }
}

resource "azurerm_app_service_custom_hostname" "frontend" {
  app_service_name = azurerm_app_service.frontend.name
  resource_group_name = var.resource_group_name
  hostname            = "media-assistant.yourdomain.com"
}
