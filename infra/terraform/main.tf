terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.80"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "staging"
}

variable "allowed_https_cidrs" {
  type        = list(string)
  description = "CIDRs permitted to reach the load balancer on 443. 0.0.0.0/0 is allowed only on 443."
  default     = ["0.0.0.0/0"]
}

resource "aws_kms_key" "orderflow" {
  description             = "Orderflow encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true
}

resource "aws_kms_alias" "orderflow" {
  name          = "alias/orderflow-${var.environment}"
  target_key_id = aws_kms_key.orderflow.key_id
}

resource "aws_vpc" "orderflow" {
  cidr_block           = "10.40.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "orderflow-${var.environment}"
  }
}

resource "aws_flow_log" "vpc" {
  vpc_id               = aws_vpc.orderflow.id
  traffic_type         = "ALL"
  log_destination_type = "cloud-watch-logs"
  log_destination      = aws_cloudwatch_log_group.vpc.arn
  iam_role_arn         = aws_iam_role.vpc_flow.arn
}

resource "aws_cloudwatch_log_group" "vpc" {
  name              = "/orderflow/${var.environment}/vpc-flow"
  retention_in_days = 365
  kms_key_id        = aws_kms_key.orderflow.arn
}

resource "aws_iam_role" "vpc_flow" {
  name = "orderflow-vpc-flow-${var.environment}"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "vpc-flow-logs.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "vpc_flow" {
  name = "orderflow-vpc-flow"
  role = aws_iam_role.vpc_flow.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["logs:CreateLogStream", "logs:PutLogEvents", "logs:DescribeLogGroups", "logs:DescribeLogStreams"]
      Resource = "${aws_cloudwatch_log_group.vpc.arn}:*"
    }]
  })
}

resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.orderflow.id
  cidr_block        = "10.40.1.0/24"
  availability_zone = "${var.aws_region}a"
}

resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.orderflow.id
  cidr_block        = "10.40.2.0/24"
  availability_zone = "${var.aws_region}b"
}

resource "aws_security_group" "alb" {
  name        = "orderflow-alb-${var.environment}"
  description = "HTTPS only from the internet"
  vpc_id      = aws_vpc.orderflow.id
}

resource "aws_security_group_rule" "alb_ingress_https" {
  type              = "ingress"
  description       = "HTTPS"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = var.allowed_https_cidrs
  security_group_id = aws_security_group.alb.id
}

resource "aws_security_group_rule" "alb_egress_app" {
  type                     = "egress"
  description              = "App traffic"
  from_port                = 8000
  to_port                  = 8000
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.app.id
  security_group_id        = aws_security_group.alb.id
}

resource "aws_security_group" "app" {
  name        = "orderflow-app-${var.environment}"
  description = "App instances accept traffic only from the ALB"
  vpc_id      = aws_vpc.orderflow.id
}

resource "aws_security_group_rule" "app_ingress_alb" {
  type                     = "ingress"
  description              = "From ALB"
  from_port                = 8000
  to_port                  = 8000
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.alb.id
  security_group_id        = aws_security_group.app.id
}

resource "aws_security_group_rule" "app_egress_db" {
  type                     = "egress"
  description              = "Postgres"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.db.id
  security_group_id        = aws_security_group.app.id
}

resource "aws_security_group" "db" {
  name        = "orderflow-db-${var.environment}"
  description = "Database accepts traffic only from the app security group"
  vpc_id      = aws_vpc.orderflow.id
}

resource "aws_security_group_rule" "db_ingress_app" {
  type                     = "ingress"
  description              = "Postgres from app"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.app.id
  security_group_id        = aws_security_group.db.id
}

resource "aws_s3_bucket" "logs" {
  bucket = "orderflow-logs-${var.environment}"
}

resource "aws_s3_bucket" "assets" {
  bucket = "orderflow-assets-${var.environment}"
}

resource "aws_s3_bucket_public_access_block" "logs" {
  bucket                  = aws_s3_bucket.logs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "assets" {
  bucket                  = aws_s3_bucket.assets.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.orderflow.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "assets" {
  bucket = aws_s3_bucket.assets.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.orderflow.arn
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_versioning" "logs" {
  bucket = aws_s3_bucket.logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "assets" {
  bucket = aws_s3_bucket.assets.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_logging" "assets" {
  bucket        = aws_s3_bucket.assets.id
  target_bucket = aws_s3_bucket.logs.id
  target_prefix = "assets/"
}

resource "aws_s3_bucket_ownership_controls" "assets" {
  bucket = aws_s3_bucket.assets.id
  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_db_subnet_group" "orderflow" {
  name       = "orderflow-${var.environment}"
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]
}

resource "aws_db_instance" "orderflow" {
  identifier                          = "orderflow-${var.environment}"
  engine                              = "postgres"
  engine_version                      = "16"
  instance_class                      = "db.t4g.micro"
  allocated_storage                   = 20
  storage_encrypted                   = true
  kms_key_id                          = aws_kms_key.orderflow.arn
  db_subnet_group_name                = aws_db_subnet_group.orderflow.name
  vpc_security_group_ids              = [aws_security_group.db.id]
  publicly_accessible                 = false
  backup_retention_period             = 7
  deletion_protection                 = true
  auto_minor_version_upgrade          = true
  iam_database_authentication_enabled = true
  manage_master_user_password         = true
  username                            = "orderflow"
  skip_final_snapshot                 = false
  final_snapshot_identifier           = "orderflow-${var.environment}-final"
  copy_tags_to_snapshot               = true
  multi_az                            = false
}

resource "aws_ebs_volume" "app_data" {
  availability_zone = "${var.aws_region}a"
  size              = 20
  type              = "gp3"
  encrypted         = true
  kms_key_id        = aws_kms_key.orderflow.arn
}

output "assets_bucket" {
  value = aws_s3_bucket.assets.bucket
}

output "database_identifier" {
  value = aws_db_instance.orderflow.identifier
}
