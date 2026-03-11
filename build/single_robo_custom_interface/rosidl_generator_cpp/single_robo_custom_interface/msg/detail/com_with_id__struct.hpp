// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from single_robo_custom_interface:msg/ComWithID.idl
// generated code does not contain a copyright notice

#ifndef SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__STRUCT_HPP_
#define SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__single_robo_custom_interface__msg__ComWithID __attribute__((deprecated))
#else
# define DEPRECATED__single_robo_custom_interface__msg__ComWithID __declspec(deprecated)
#endif

namespace single_robo_custom_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ComWithID_
{
  using Type = ComWithID_<ContainerAllocator>;

  explicit ComWithID_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->com_arr.begin(), this->com_arr.end(), 0.0);
      this->id = 0l;
    }
  }

  explicit ComWithID_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : com_arr(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->com_arr.begin(), this->com_arr.end(), 0.0);
      this->id = 0l;
    }
  }

  // field types and members
  using _com_arr_type =
    std::array<double, 3>;
  _com_arr_type com_arr;
  using _id_type =
    int32_t;
  _id_type id;

  // setters for named parameter idiom
  Type & set__com_arr(
    const std::array<double, 3> & _arg)
  {
    this->com_arr = _arg;
    return *this;
  }
  Type & set__id(
    const int32_t & _arg)
  {
    this->id = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    single_robo_custom_interface::msg::ComWithID_<ContainerAllocator> *;
  using ConstRawPtr =
    const single_robo_custom_interface::msg::ComWithID_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<single_robo_custom_interface::msg::ComWithID_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<single_robo_custom_interface::msg::ComWithID_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      single_robo_custom_interface::msg::ComWithID_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<single_robo_custom_interface::msg::ComWithID_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      single_robo_custom_interface::msg::ComWithID_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<single_robo_custom_interface::msg::ComWithID_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<single_robo_custom_interface::msg::ComWithID_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<single_robo_custom_interface::msg::ComWithID_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__single_robo_custom_interface__msg__ComWithID
    std::shared_ptr<single_robo_custom_interface::msg::ComWithID_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__single_robo_custom_interface__msg__ComWithID
    std::shared_ptr<single_robo_custom_interface::msg::ComWithID_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ComWithID_ & other) const
  {
    if (this->com_arr != other.com_arr) {
      return false;
    }
    if (this->id != other.id) {
      return false;
    }
    return true;
  }
  bool operator!=(const ComWithID_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ComWithID_

// alias to use template instance with default allocator
using ComWithID =
  single_robo_custom_interface::msg::ComWithID_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace single_robo_custom_interface

#endif  // SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__COM_WITH_ID__STRUCT_HPP_
