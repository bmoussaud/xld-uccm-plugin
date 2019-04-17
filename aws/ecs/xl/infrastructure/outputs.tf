output "address" {
  value = "${aws_alb.ecs-alb.dns_name}"
}

output "execution_role_arn" {
  value = "${aws_iam_role.ecs-task-execution-role.arn}"
}

output "alb_tg_arn" {
  value = "${aws_alb_target_group.ecs-alb-tg.arn}"
}

output "cluster_arn" {
  value = "${aws_ecs_cluster.ecs-cluster.arn}"
}
