import { create } from 'naive-ui'
import type { App } from 'vue'

import {
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NLayoutFooter,
  NLayoutSider,
  NGrid,
  NGridItem,
  NGi,
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
  NMenu,
  NDropdown,
  NBreadcrumb,
  NBreadcrumbItem,
  NPagination,
  NTabs,
  NTabPane,
  NForm,
  NFormItem,
  NInput,
  NInputGroup,
  NInputNumber,
  NSelect,
  NRadio,
  NRadioGroup,
  NRadioButton,
  NCheckbox,
  NCheckboxGroup,
  NSwitch,
  NDatePicker,
  NTimePicker,
  NSlider,
  NUpload,
  NUploadDragger,
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
  NConfigProvider,
  NMessageProvider,
  NDialogProvider,
  NNotificationProvider,
  NLoadingBarProvider
} from 'naive-ui'

const naive = create({
  components: [
    NLayout, NLayoutHeader, NLayoutContent, NLayoutFooter, NLayoutSider,
    NGrid, NGridItem, NGi,
    NButton, NIcon, NAvatar, NBadge, NTag, NSpace, NDivider, NRate, NText, NCode, NScrollbar,
    NMenu, NDropdown, NBreadcrumb, NBreadcrumbItem, NPagination, NTabs, NTabPane,
    NForm, NFormItem, NInput, NInputGroup, NInputNumber, NSelect,
    NRadio, NRadioGroup, NRadioButton, NCheckbox, NCheckboxGroup,
    NSwitch, NDatePicker, NTimePicker, NSlider, NUpload, NUploadDragger,
    NTable, NList, NListItem, NThing, NImage, NCard,
    NCollapse, NCollapseItem, NDescriptions, NDescriptionsItem,
    NTree, NTimeline, NTimelineItem,
    NModal, NDrawer, NDrawerContent, NPopover, NTooltip,
    NAlert, NProgress, NSpin, NResult, NEmpty,
    NConfigProvider, NMessageProvider, NDialogProvider, NNotificationProvider, NLoadingBarProvider
  ]
})

export default {
  install(app: App) {
    app.use(naive)
  }
}

export function setupNaiveUI(app: App) {
  app.use(naive)
}
