// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from single_robo_custom_interface:msg/ClusterPoints.idl
// generated code does not contain a copyright notice

#ifndef SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__FUNCTIONS_H_
#define SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "single_robo_custom_interface/msg/rosidl_generator_c__visibility_control.h"

#include "single_robo_custom_interface/msg/detail/cluster_points__struct.h"

/// Initialize msg/ClusterPoints message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * single_robo_custom_interface__msg__ClusterPoints
 * )) before or use
 * single_robo_custom_interface__msg__ClusterPoints__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
bool
single_robo_custom_interface__msg__ClusterPoints__init(single_robo_custom_interface__msg__ClusterPoints * msg);

/// Finalize msg/ClusterPoints message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
void
single_robo_custom_interface__msg__ClusterPoints__fini(single_robo_custom_interface__msg__ClusterPoints * msg);

/// Create msg/ClusterPoints message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * single_robo_custom_interface__msg__ClusterPoints__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
single_robo_custom_interface__msg__ClusterPoints *
single_robo_custom_interface__msg__ClusterPoints__create();

/// Destroy msg/ClusterPoints message.
/**
 * It calls
 * single_robo_custom_interface__msg__ClusterPoints__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
void
single_robo_custom_interface__msg__ClusterPoints__destroy(single_robo_custom_interface__msg__ClusterPoints * msg);

/// Check for msg/ClusterPoints message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
bool
single_robo_custom_interface__msg__ClusterPoints__are_equal(const single_robo_custom_interface__msg__ClusterPoints * lhs, const single_robo_custom_interface__msg__ClusterPoints * rhs);

/// Copy a msg/ClusterPoints message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
bool
single_robo_custom_interface__msg__ClusterPoints__copy(
  const single_robo_custom_interface__msg__ClusterPoints * input,
  single_robo_custom_interface__msg__ClusterPoints * output);

/// Initialize array of msg/ClusterPoints messages.
/**
 * It allocates the memory for the number of elements and calls
 * single_robo_custom_interface__msg__ClusterPoints__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
bool
single_robo_custom_interface__msg__ClusterPoints__Sequence__init(single_robo_custom_interface__msg__ClusterPoints__Sequence * array, size_t size);

/// Finalize array of msg/ClusterPoints messages.
/**
 * It calls
 * single_robo_custom_interface__msg__ClusterPoints__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
void
single_robo_custom_interface__msg__ClusterPoints__Sequence__fini(single_robo_custom_interface__msg__ClusterPoints__Sequence * array);

/// Create array of msg/ClusterPoints messages.
/**
 * It allocates the memory for the array and calls
 * single_robo_custom_interface__msg__ClusterPoints__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
single_robo_custom_interface__msg__ClusterPoints__Sequence *
single_robo_custom_interface__msg__ClusterPoints__Sequence__create(size_t size);

/// Destroy array of msg/ClusterPoints messages.
/**
 * It calls
 * single_robo_custom_interface__msg__ClusterPoints__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
void
single_robo_custom_interface__msg__ClusterPoints__Sequence__destroy(single_robo_custom_interface__msg__ClusterPoints__Sequence * array);

/// Check for msg/ClusterPoints message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
bool
single_robo_custom_interface__msg__ClusterPoints__Sequence__are_equal(const single_robo_custom_interface__msg__ClusterPoints__Sequence * lhs, const single_robo_custom_interface__msg__ClusterPoints__Sequence * rhs);

/// Copy an array of msg/ClusterPoints messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_single_robo_custom_interface
bool
single_robo_custom_interface__msg__ClusterPoints__Sequence__copy(
  const single_robo_custom_interface__msg__ClusterPoints__Sequence * input,
  single_robo_custom_interface__msg__ClusterPoints__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__FUNCTIONS_H_
