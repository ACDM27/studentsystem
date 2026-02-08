import { h } from 'vue'
import { NIcon } from 'naive-ui'
import type { Component } from 'vue'

/**
 * 渲染图标的工具函数
 * @param icon 图标组件
 * @param size 图标大小，默认为24
 * @param color 图标颜色，可选
 * @returns 渲染函数
 */
export function renderIcon(icon: Component, size: number = 24, color?: string) {
  return () => h(NIcon, 
    { 
      size, 
      color,
      style: 'display: flex; align-items: center; justify-content: flex-start;'
    }, 
    { default: () => h(icon, { size }) }
  )
}

/**
 * 渲染菜单图标的工具函数
 * @param icon 图标组件
 * @param size 图标大小，默认为24
 * @param color 图标颜色，可选
 * @returns 渲染函数
 */
export function renderMenuIcon(icon: Component, size: number = 24, color?: string) {
  return () => h(NIcon, 
    { 
      size, 
      color,
      style: 'display: flex; align-items: center; justify-content: flex-start;'
    }, 
    { default: () => h(icon, { size }) }
  )
}

/**
 * 渲染按钮图标的工具函数
 * @param icon 图标组件
 * @param size 图标大小，默认为18
 * @param color 图标颜色，可选
 * @returns 渲染函数
 */
export function renderButtonIcon(icon: Component, size: number = 18, color?: string) {
  return () => h(NIcon, 
    { 
      size, 
      color,
      style: 'display: flex; align-items: center; justify-content: center;'
    }, 
    { default: () => h(icon, { size }) }
  )
}