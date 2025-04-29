resource "null_resource" "default" {
  provisioner "local-exec" {
    command = "az acr login --name ${var.registry_name}"
  }

  provisioner "local-exec" {
    command = "docker build -t ${var.registry_login_server}/${var.image_name}:latest --file ../apserver/Dockerfile ../apserver/"
  }
  provisioner "local-exec" {
    command = "docker push ${var.registry_login_server}/${var.image_name}:latest"
  }
}
