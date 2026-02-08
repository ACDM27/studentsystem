import { create } from 'naive-ui'
import type { App } from 'vue'

// 导入所需的Naive UI组件
import {
  // 布局组件
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NLayoutFooter,
  NLayoutSider,
  NGrid,
  NGridItem,
  NGi,
  
  // 基础组件
  NButton,
  NIcon,
  NAvatar,
  NBadge,
  NTag,
  NSpace,
  NDivider,
  NRate,
  NText,
  NCode,
  NScrollbar,
  
  // 导航组件
  NMenu,
  NDropdown,
  NBreadcrumb,
  NBreadcrumbItem,
  NPagination,
  NTabs,
  NTabPane,
  
  // 数据输入组件
  NForm,
  NFormItem,
  NInput,
  NInputGroup,
  NInputNumber,
  NSelect,
  NRadio,
  NRadioGroup,
  NCheckbox,
  NCheckboxGroup,
  NSwitch,
  NDatePicker,
  NTimePicker,
  NSlider,
  NUpload,
  
  // 数据展示组件
  NTable,
  NList,
  NListItem,
  NThing,
  NImage,
  NCard,
  NCollapse,
  NCollapseItem,
  NDescriptions,
  NDescriptionsItem,
  NTree,
  NTimeline,
  NTimelineItem,
  
  // 反馈组件
  NModal,
  NDrawer,
  NDrawerContent,
  NPopover,
  NTooltip,
  NAlert,
  NProgress,
  NSpin,
  NResult,
  NEmpty,
  
  // 配置组件
  NConfigProvider,
  NMessageProvider,
  NDialogProvider,
  NNotificationProvider,
  NLoadingBarProvider
} from 'naive-ui'

// 创建Naive UI实例并注册所有组件
const naive = create({
  components: [
    // 布局组件
    NLayout,
    NLayoutHeader,
    NLayoutContent,
    NLayoutFooter,
    NLayoutSider,
    NGrid,
    NGridItem,
    NGi,
    
    // 基础组件
    NButton,
    NIcon,
    NAvatar,
    NBadge,
    NTag,
    NSpace,
    NDivider,
    NRate,
    NText,
    NCode,
    NScrollbar,
    
    // 导航组件
    NMenu,
    NDropdown,
    NBreadcrumb,
    NBreadcrumbItem,
    NPagination,
    NTabs,
    NTabPane,
    
    // 数据输入组件
    NForm,
    NFormItem,
    NInput,
    NInputGroup,
    NInputNumber,
    NSelect,
    NRadio,
    NRadioGroup,
    NCheckbox,
    NCheckboxGroup,
    NSwitch,
    NDatePicker,
    NTimePicker,
    NSlider,
    NUpload,
    
    // 数据展示组件
    NTable,
    NList,
    NListItem,
    NThing,
    NImage,
    NCard,
    NCollapse,
    NCollapseItem,
    NDescriptions,
    NDescriptionsItem,
    NTree,
    NTimeline,
    NTimelineItem,
    
    // 反馈组件
  NModal,
  NDrawer,
  NDrawerContent,
  NPopover,
    NTooltip,
    NAlert,
    NProgress,
    NSpin,
    NResult,
    NEmpty,
    
    // 配置组件
    NConfigProvider,
    NMessageProvider,
    NDialogProvider,
    NNotificationProvider,
    NLoadingBarProvider
  ]
})

// 导出插件安装函数
export default {
  install(app: App) {
    app.use(naive)
  }
}

// 导出一个函数用于按需注册组件
export function setupNaiveUI(app: App) {
  app.use(naive)
}