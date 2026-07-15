terraform {
  cloud {
    organization = "kieranhogg"
    workspaces {
      name = "staging"
    }
  }

  required_providers {
    proxmox = {
      source  = "telmate/proxmox"
      version = "3.0.2-rc08"
    }
  }
}
provider "proxmox" {
  pm_api_url          = "https://10.0.0.244:8006/api2/json"
  pm_api_token_id     = var.proxmox_id
  pm_api_token_secret = var.proxmox_token
  pm_tls_insecure     = true
}

# Proxmox VM setup
resource "proxmox_vm_qemu" "staging_node" {
  name        = "wotd"
  target_node = "pve"
  clone       = "temp-ubuntu-26-04"
  full_clone  = true

  bios    = "ovmf"
  machine = "q35"
  scsihw  = "virtio-scsi-single"
  boot    = "order=scsi0"

  cpu {
    cores = 2
  }
  memory  = 2048
  agent   = 1
  os_type = "cloud-init"

  disk {
    slot    = "scsi0"
    storage = "local"
    size    = "20G"
    type    = "disk"
  }

  disk {
    slot    = "ide2"
    storage = "local"
    type    = "cloudinit"
  }

  efidisk {
    storage           = "local"
    efitype           = "4m"
    pre_enrolled_keys = true
  }

  serial {
    id   = 0
    type = "socket"
  }
  network {
    id     = 0
    model  = "virtio"
    bridge = "vmbr0"
  }
  ciuser           = "user"
  sshkeys          = var.ssh_public_key
  ipconfig0        = "ip=10.0.0.44/24,gw=10.0.0.160"
  automatic_reboot = true
}

output "vm_ip" {
  value = proxmox_vm_qemu.staging_node.default_ipv4_address
}

# Inventory creation
resource "local_file" "ansible_staging_inventory" {
  filename = "${path.module}/../../ansible/staging.ini"
  content  = <<EOT
[staging]
${proxmox_vm_qemu.staging_node.default_ipv4_address} ansible_user=user

[staging:vars]
env_caddyfile=../../terraform/staging/Caddyfile
EOT
}
