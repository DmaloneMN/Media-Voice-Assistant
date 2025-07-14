output "cosmosdb_connection_string" {
  value     = azurerm_cosmosdb_account.main.connection_strings[0]
  sensitive = true
}

output "cosmosdb_endpoint" {
  value = azurerm_cosmosdb_account.main.endpoint
}
