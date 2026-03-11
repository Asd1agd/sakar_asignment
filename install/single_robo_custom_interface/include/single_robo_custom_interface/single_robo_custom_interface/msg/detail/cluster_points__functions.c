// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from single_robo_custom_interface:msg/ClusterPoints.idl
// generated code does not contain a copyright notice
#include "single_robo_custom_interface/msg/detail/cluster_points__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
single_robo_custom_interface__msg__ClusterPoints__init(single_robo_custom_interface__msg__ClusterPoints * msg)
{
  if (!msg) {
    return false;
  }
  // points_arr
  return true;
}

void
single_robo_custom_interface__msg__ClusterPoints__fini(single_robo_custom_interface__msg__ClusterPoints * msg)
{
  if (!msg) {
    return;
  }
  // points_arr
}

bool
single_robo_custom_interface__msg__ClusterPoints__are_equal(const single_robo_custom_interface__msg__ClusterPoints * lhs, const single_robo_custom_interface__msg__ClusterPoints * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // points_arr
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->points_arr[i] != rhs->points_arr[i]) {
      return false;
    }
  }
  return true;
}

bool
single_robo_custom_interface__msg__ClusterPoints__copy(
  const single_robo_custom_interface__msg__ClusterPoints * input,
  single_robo_custom_interface__msg__ClusterPoints * output)
{
  if (!input || !output) {
    return false;
  }
  // points_arr
  for (size_t i = 0; i < 3; ++i) {
    output->points_arr[i] = input->points_arr[i];
  }
  return true;
}

single_robo_custom_interface__msg__ClusterPoints *
single_robo_custom_interface__msg__ClusterPoints__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  single_robo_custom_interface__msg__ClusterPoints * msg = (single_robo_custom_interface__msg__ClusterPoints *)allocator.allocate(sizeof(single_robo_custom_interface__msg__ClusterPoints), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(single_robo_custom_interface__msg__ClusterPoints));
  bool success = single_robo_custom_interface__msg__ClusterPoints__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
single_robo_custom_interface__msg__ClusterPoints__destroy(single_robo_custom_interface__msg__ClusterPoints * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    single_robo_custom_interface__msg__ClusterPoints__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
single_robo_custom_interface__msg__ClusterPoints__Sequence__init(single_robo_custom_interface__msg__ClusterPoints__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  single_robo_custom_interface__msg__ClusterPoints * data = NULL;

  if (size) {
    data = (single_robo_custom_interface__msg__ClusterPoints *)allocator.zero_allocate(size, sizeof(single_robo_custom_interface__msg__ClusterPoints), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = single_robo_custom_interface__msg__ClusterPoints__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        single_robo_custom_interface__msg__ClusterPoints__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
single_robo_custom_interface__msg__ClusterPoints__Sequence__fini(single_robo_custom_interface__msg__ClusterPoints__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      single_robo_custom_interface__msg__ClusterPoints__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

single_robo_custom_interface__msg__ClusterPoints__Sequence *
single_robo_custom_interface__msg__ClusterPoints__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  single_robo_custom_interface__msg__ClusterPoints__Sequence * array = (single_robo_custom_interface__msg__ClusterPoints__Sequence *)allocator.allocate(sizeof(single_robo_custom_interface__msg__ClusterPoints__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = single_robo_custom_interface__msg__ClusterPoints__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
single_robo_custom_interface__msg__ClusterPoints__Sequence__destroy(single_robo_custom_interface__msg__ClusterPoints__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    single_robo_custom_interface__msg__ClusterPoints__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
single_robo_custom_interface__msg__ClusterPoints__Sequence__are_equal(const single_robo_custom_interface__msg__ClusterPoints__Sequence * lhs, const single_robo_custom_interface__msg__ClusterPoints__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!single_robo_custom_interface__msg__ClusterPoints__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
single_robo_custom_interface__msg__ClusterPoints__Sequence__copy(
  const single_robo_custom_interface__msg__ClusterPoints__Sequence * input,
  single_robo_custom_interface__msg__ClusterPoints__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(single_robo_custom_interface__msg__ClusterPoints);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    single_robo_custom_interface__msg__ClusterPoints * data =
      (single_robo_custom_interface__msg__ClusterPoints *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!single_robo_custom_interface__msg__ClusterPoints__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          single_robo_custom_interface__msg__ClusterPoints__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!single_robo_custom_interface__msg__ClusterPoints__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
