provider "aws" {
  region = "eu-west-1"
  profile = "voismgmt"
}

data "aws_autoscaling_groups" "groups" {
  filter {
    name   = "tag-key"
    values = ["TurnOff"]
  }

#filter {
 #   name   = "tag-value"
  #  values = ["True"]
  #}

}


resource "aws_autoscaling_schedule" "startscaling" {
  count = length(data.aws_autoscaling_groups.groups.names)
  scheduled_action_name  = "startscaling-2-zero"
  min_size               = 0
  max_size               = 0
  desired_capacity       = 0
  recurrence             = "00 17 * * 1-5"
  end_time               = "2099-12-12T06:00:00Z"
  time_zone              = "UTC"
  autoscaling_group_name = data.aws_autoscaling_groups.groups.names[count.index]
}


resource "aws_autoscaling_schedule" "stopscaling" {
  count = length(data.aws_autoscaling_groups.groups.names)
  scheduled_action_name  = "stopscaling-2-zero"
  min_size               = 2
  max_size               = 4
  desired_capacity       = 2
  recurrence             = "00 5 * * 1-5"
  end_time               = "2099-12-12T06:00:00Z"
  time_zone              = "UTC"
  autoscaling_group_name = data.aws_autoscaling_groups.groups.names[count.index]
}

output "au22" {
  value = data.aws_autoscaling_groups.groups.names
}
