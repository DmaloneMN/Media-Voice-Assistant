output "frontend_url" {
  description = "URL of the frontend web app"
  value       = azurerm_static_site.frontend.default_host_name
}

output "api_endpoint" {
  description = "URL of the API endpoint"
  value       = azurerm_function_app.backend.default_hostname
}

output "cosmosdb_connection_string" {
  description = "Cosmos DB connection string"
  value       = azurerm_cosmosdb_account.main.connection_strings[0]
  sensitive   = true
}

output "speech_key" {
  description = "Cognitive Services Speech key"
  value       = azurerm_cognitive_account.speech.primary_access_key
  sensitive   = true
}
