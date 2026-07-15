variable "proxmox_token" {
  type        = string
  description = "Proxmox API Key"
  sensitive   = true
}
variable "ssh_public_key" {
  type        = string
  description = "SSH key used to access staging"

}
