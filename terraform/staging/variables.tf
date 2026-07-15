variable "proxmox_token" {
  type        = string
  description = "Proxmox API Key"
  sensitive   = true
}
variable "proxmox_id" {
  type        = string
  description = "Proxmox API ID"
  sensitive   = true
}
variable "ssh_public_key" {
  type        = string
  description = "SSH key used to access staging"

}
