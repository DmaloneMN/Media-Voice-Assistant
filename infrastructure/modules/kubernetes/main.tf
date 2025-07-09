# In infrastructure/modules/kubernetes/main.tf
resource "azurerm_kubernetes_cluster_node_pool" "user_pool" {
  name                  = "userpool"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.main.id
  vm_size               = "Standard_DS3_v2"
  node_count            = var.node_count
  enable_auto_scaling   = true
  min_count            = 2
  max_count            = 10
}
