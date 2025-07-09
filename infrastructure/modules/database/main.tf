resource "azurerm_cosmosdb_sql_container" "media" {
  name                = "MediaCatalog"
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_path  = "/partitionKey"
  throughput          = 400

  indexing_policy {
    indexing_mode = "consistent"

    included_path {
      path = "/*"
    }
  }
}

# Add a separate container for user preferences
resource "azurerm_cosmosdb_sql_container" "user_preferences" {
  name                = "UserPreferences"
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_path  = "/userId"
  throughput          = 400
}
