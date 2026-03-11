// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from single_robo_custom_interface:msg/ComWithID.idl
// generated code does not contain a copyright notice

#ifndef SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__BUILDER_HPP_
#define SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "single_robo_custom_interface/msg/detail/com_with_id__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace single_robo_custom_interface
{

namespace msg
{

namespace builder
{

class Init_ComWithID_id
{
public:
  explicit Init_ComWithID_id(::single_robo_custom_interface::msg::ComWithID & msg)
  : msg_(msg)
  {}
  ::single_robo_custom_interface::msg::ComWithID id(::single_robo_custom_interface::msg::ComWithID::_id_type arg)
  {
    msg_.id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::single_robo_custom_interface::msg::ComWithID msg_;
};

class Init_ComWithID_com_arr
{
public:
  Init_ComWithID_com_arr()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ComWithID_id com_arr(::single_robo_custom_interface::msg::ComWithID::_com_arr_type arg)
  {
    msg_.com_arr = std::move(arg);
    return Init_ComWithID_id(msg_);
  }

private:
  ::single_robo_custom_interface::msg::ComWithID msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::single_robo_custom_interface::msg::ComWithID>()
{
  return single_robo_custom_interface::msg::builder::Init_ComWithID_com_arr();
}

}  // namespace single_robo_custom_interface

#endif  // SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__BUILDER_HPP_
