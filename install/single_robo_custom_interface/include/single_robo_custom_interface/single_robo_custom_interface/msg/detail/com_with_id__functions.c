// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from single_robo_custom_interface:msg/ComWithID.idl
// generated code does not contain a copyright notice
#include "single_robo_custom_interface/msg/detail/com_with_id__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
single_robo_custom_interface__msg__ComWithID__init(single_robo_custom_interface__msg__ComWithID * msg)
{
  if (!msg) {
    return false;
  }
  // com_arr
  // id
  return true;
}

void
single_robo_custom_interface__msg__ComWithID__fini(single_robo_custom_interface__msg__ComWithID * msg)
{
  if (!msg) {
    return;
  }
  // com_arr
  // id
}

bool
single_robo_custom_interface__msg__ComWithID__are_equal(const single_robo_custom_interface__msg__ComWithID * lhs, const single_robo_custom_interface__msg__ComWithID * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // com_arr
  for (size_t i = 0; i < 3; ++i) {
    if (lhs->com_arr[i] != rhs->com_arr[i]) {
      return false;
    }
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  return true;
}

bool
single_robo_custom_interface__msg__ComWithID__copy(
  const single_robo_custom_interface__msg__ComWithID * input,
  single_robo_custom_interface__msg__ComWithID * output)
{
  if (!input || !output) {
    return false;
  }
  // com_arr
  for (size_t i = 0; i < 3; ++i) {
    output->com_arr[i] = input->com_arr[i];
  }
  // id
  output->id = input->id;
  return true;
}

single_robo_custom_interface__msg__ComWithID *
single_robo_custom_interface__msg__ComWithID__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  single_robo_custom_interface__msg__ComWithID * msg = (single_robo_custom_interface__msg__ComWithID *)allocator.allocate(sizeof(single_robo_custom_interface__msg__ComWithID), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(single_robo_custom_interface__msg__ComWithID));
  bool success = single_robo_custom_interface__msg__ComWithID__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
single_robo_custom_interface__msg__ComWithID__destroy(single_robo_custom_interface__msg__ComWithID * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    single_robo_custom_interface__msg__ComWithID__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
single_robo_custom_interface__msg__ComWithID__Sequence__init(single_robo_custom_interface__msg__ComWithID__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  single_robo_custom_interface__msg__ComWithID * data = NULL;

  if (size) {
    data = (single_robo_custom_interface__msg__ComWithID *)allocator.zero_allocate(size, sizeof(single_robo_custom_interface__msg__ComWithID), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = single_robo_custom_interface__msg__ComWithID__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        single_robo_custom_interface__msg__ComWithID__fini(&data[i - 1]);
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
single_robo_custom_interface__msg__ComWithID__Sequence__fini(single_robo_custom_interface__msg__ComWithID__Sequence * array)
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
      single_robo_custom_interface__msg__ComWithID__fini(&array->data[i]);
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

single_robo_custom_interface__msg__ComWithID__Sequence *
single_robo_custom_interface__msg__ComWithID__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  single_robo_custom_interface__msg__ComWithID__Sequence * array = (single_robo_custom_interface__msg__ComWithID__Sequence *)allocator.allocate(sizeof(single_robo_custom_interface__msg__ComWithID__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = single_robo_custom_interface__msg__ComWithID__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
single_robo_custom_interface__msg__ComWithID__Sequence__destroy(single_robo_custom_interface__msg__ComWithID__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    single_robo_custom_interface__msg__ComWithID__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
single_robo_custom_interface__msg__ComWithID__Sequence__are_equal(const single_robo_custom_interface__msg__ComWithID__Sequence * lhs, const single_robo_custom_interface__msg__ComWithID__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!single_robo_custom_interface__msg__ComWithID__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
single_robo_custom_interface__msg__ComWithID__Sequence__copy(
  const single_robo_custom_interface__msg__ComWithID__Sequence * input,
  single_robo_custom_interface__msg__ComWithID__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(single_robo_custom_interface__msg__ComWithID);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    single_robo_custom_interface__msg__ComWithID * data =
      (single_robo_custom_interface__msg__ComWithID *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!single_robo_custom_interface__msg__ComWithID__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          single_robo_custom_interface__msg__ComWithID__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!single_robo_custom_interface__msg__ComWithID__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
