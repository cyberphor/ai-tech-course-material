output "url" {
  value = [
    "https://${azurerm_linux_function_app.main.default_hostname}/api/llm?message='hello'",
  ]
}
