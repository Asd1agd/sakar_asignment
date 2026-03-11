// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from single_robo_custom_interface:msg/ComWithID.idl
// generated code does not contain a copyright notice

#ifndef SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "single_robo_custom_interface/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "single_robo_custom_interface/msg/detail/com_with_id__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace single_robo_custom_interface
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_single_robo_custom_interface
cdr_serialize(
  const single_robo_custom_interface::msg::ComWithID & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_single_robo_custom_interface
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  single_robo_custom_interface::msg::ComWithID & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_single_robo_custom_interface
get_serialized_size(
  const single_robo_custom_interface::msg::ComWithID & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_single_robo_custom_interface
max_serialized_size_ComWithID(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace single_robo_custom_interface

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_single_robo_custom_interface
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, single_robo_custom_interface, msg, ComWithID)();

#ifdef __cplusplus
}
#endif

#endif  // SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
