resource "azurerm_kubernetes_cluster" "main" {
  name                = var.cluster_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = "${var.cluster_name}-dns"
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name       = "default"
    node_count = var.node_count
    vm_size    = var.vm_size
  }

  # Choose ONE of these identity options (not both):

  # Option 1: System-assigned managed identity (recommended)
  identity {
    type = "SystemAssigned"
  }

  # Option 2: Service principal (only use if you have specific requirements)
  # service_principal {
  #   client_id     = var.client_id
  #   client_secret = var.client_secret
  # }

  network_profile {
    network_plugin = "kubenet"
    network_policy = "calico"
  }
}
