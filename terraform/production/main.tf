terraform {
  cloud {
    organization = "kieranhogg"
    workspaces {
      name = "prod"
    }
  }
  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.45"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token
}

data "hcloud_ssh_key" "my_key" {
  name = "macbook"
}

resource "hcloud_server" "production_node" {
  name        = "fastapi-prod-01"
  image       = "ubuntu-24.04"
  server_type = "cx23"
  location    = "nbg1"
  ssh_keys    = [data.hcloud_ssh_key.my_key.id]
}

output "production_ip" {
  description = "The public IP of your new server"
  value       = hcloud_server.production_node.ipv4_address
}

# Inventory creation
resource "local_file" "ansible_production_inventory" {
  filename = "${path.module}/../../ansible/production.ini"
  content  = <<EOT
[production]
${hcloud_server.production_node.ipv4_address} ansible_user=root

[production:vars]
env_caddyfile=../../terraform/production/Caddyfile
EOT
}
