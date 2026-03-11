// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from single_robo_custom_interface:msg/ComWithID.idl
// generated code does not contain a copyright notice

#ifndef SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__STRUCT_H_
#define SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ComWithID in the package single_robo_custom_interface.
/**
  * nearest_cluster_centroid_point = [x, y, z], id
 */
typedef struct single_robo_custom_interface__msg__ComWithID
{
  double com_arr[3];
  int32_t id;
} single_robo_custom_interface__msg__ComWithID;

// Struct for a sequence of single_robo_custom_interface__msg__ComWithID.
typedef struct single_robo_custom_interface__msg__ComWithID__Sequence
{
  single_robo_custom_interface__msg__ComWithID * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} single_robo_custom_interface__msg__ComWithID__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__STRUCT_H_
