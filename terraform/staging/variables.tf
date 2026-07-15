variable "proxmox_token_secret" {
  type        = string
  description = "Proxmox API Key"
  sensitive   = true
}
variable "proxmox_token_id" {
  type        = string
  description = "Proxmox API ID"
  sensitive   = true
}
variable "ssh_public_key" {
  type        = string
  description = "SSH key used to access staging"
}
