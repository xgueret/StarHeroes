resource "github_repository" "startheroes" {
  name        = var.repository_name
  description = var.repository_description
  visibility  = var.visibility
}

output "repository_url" {
  value = github_repository.startheroes.html_url
}