variable "cluster_name" {
  description = "Name of the AKS cluster"
  type        = string
}

variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "node_count" {
  description = "Number of AKS nodes"
  type        = number
  default     = 2
}

variable "vm_size" {
  description = "VM size for nodes"
  type        = string
  default     = "Standard_D2_v2"
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.26"
}

# Only needed if using service principal
# variable "client_id" {
#   description = "Service principal client ID"
#   type        = string
#   sensitive   = true
# }

# variable "client_secret" {
#   description = "Service principal client secret"
#   type        = string
#   sensitive   = true
# }
