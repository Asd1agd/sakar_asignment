// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from single_robo_custom_interface:msg/ClusterPoints.idl
// generated code does not contain a copyright notice

#ifndef SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__STRUCT_H_
#define SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ClusterPoints in the package single_robo_custom_interface.
/**
  * x_w, y_w, z_w world coordinates
 */
typedef struct single_robo_custom_interface__msg__ClusterPoints
{
  double points_arr[3];
} single_robo_custom_interface__msg__ClusterPoints;

// Struct for a sequence of single_robo_custom_interface__msg__ClusterPoints.
typedef struct single_robo_custom_interface__msg__ClusterPoints__Sequence
{
  single_robo_custom_interface__msg__ClusterPoints * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} single_robo_custom_interface__msg__ClusterPoints__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__STRUCT_H_
