// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from single_robo_custom_interface:msg/ClusterPoints.idl
// generated code does not contain a copyright notice

#ifndef SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__STRUCT_HPP_
#define SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__single_robo_custom_interface__msg__ClusterPoints __attribute__((deprecated))
#else
# define DEPRECATED__single_robo_custom_interface__msg__ClusterPoints __declspec(deprecated)
#endif

namespace single_robo_custom_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ClusterPoints_
{
  using Type = ClusterPoints_<ContainerAllocator>;

  explicit ClusterPoints_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->points_arr.begin(), this->points_arr.end(), 0.0);
    }
  }

  explicit ClusterPoints_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : points_arr(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      std::fill<typename std::array<double, 3>::iterator, double>(this->points_arr.begin(), this->points_arr.end(), 0.0);
    }
  }

  // field types and members
  using _points_arr_type =
    std::array<double, 3>;
  _points_arr_type points_arr;

  // setters for named parameter idiom
  Type & set__points_arr(
    const std::array<double, 3> & _arg)
  {
    this->points_arr = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator> *;
  using ConstRawPtr =
    const single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__single_robo_custom_interface__msg__ClusterPoints
    std::shared_ptr<single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__single_robo_custom_interface__msg__ClusterPoints
    std::shared_ptr<single_robo_custom_interface::msg::ClusterPoints_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ClusterPoints_ & other) const
  {
    if (this->points_arr != other.points_arr) {
      return false;
    }
    return true;
  }
  bool operator!=(const ClusterPoints_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ClusterPoints_

// alias to use template instance with default allocator
using ClusterPoints =
  single_robo_custom_interface::msg::ClusterPoints_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace single_robo_custom_interface

#endif  // SINGLE_ROBO_CUSTOM_INTERFACE__MSG__DETAIL__CLUSTER_POINTS__STRUCT_HPP_
