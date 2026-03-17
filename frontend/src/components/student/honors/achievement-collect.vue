<template>
  <div class="collect_page">
    <!-- 页面标题区域 -->
    <header class="header">
      <div class="header_top">
        <n-button text size="large" @click="go_back" class="back_btn">
          <template #icon><ArrowLeft :size="20" /></template>
          {{ collect_type ? '重新选择类型' : '返回成果展示' }}
        </n-button>
      </div>
      <h1>成果收集</h1>
      <p>{{ collect_type === 'paper' ? '填写论文成果信息' : collect_type === 'patent' ? '填写专利成果信息' : collect_type === 'certificate' ? '填写证书/竞赛成果信息' : '选择要收集的成果类型' }}</p>
    </header>

    <!-- 步骤零：类型选择 -->
    <div v-if="!collect_type" class="type_select">
      <div class="type_grid">
        <div class="type_card" @click="collect_type = 'certificate'">
          <div class="type_icon certificate_icon">
            <Award :size="40" />
          </div>
          <div class="type_title">证书 / 竞赛奖项</div>
          <div class="type_desc">荣誉证书、获奖证书、学科竞赛、技能认证等</div>
          <div class="type_action">开始填写 →</div>
        </div>
        <div class="type_card" @click="collect_type = 'paper'">
          <div class="type_icon paper_icon">
            <FileText :size="40" />
          </div>
          <div class="type_title">学术论文</div>
          <div class="type_desc">期刊论文、会议论文等学术成果</div>
          <div class="type_action">开始填写 →</div>
        </div>
        <div class="type_card" @click="collect_type = 'patent'">
          <div class="type_icon patent_icon">
            <Bulb :size="40" />
          </div>
          <div class="type_title">专利 / 软件著作权</div>
          <div class="type_desc">发明专利、实用新型专利、外观设计专利、软件著作权等</div>
          <div class="type_action">开始填写 →</div>
        </div>
      </div>
    </div>

    <!-- 证书/竞赛表单 -->
    <n-card v-if="collect_type === 'certificate'" class="form_card">
      <n-form 
        ref="form_ref" 
        :model="form_data" 
        :rules="form_rules" 
        label-placement="top"
        require-mark-placement="right-hanging"
        size="medium"
      >
        <!-- OCR 快速识别 -->
        <div class="form_section ocr_hint_section">
          <h3 class="section_title"><Scan :size="20" />AI 快速识别（可选）</h3>
          <p style="margin: 0 0 12px; color: #666; font-size: 13px;">
            请先选择成果类别，再上传证书图片，AI 将按类型自动提取对应字段
          </p>
          <n-upload
            :custom-request="handle_cert_ocr"
            :show-file-list="false"
            accept=".jpg,.jpeg,.png"
            :disabled="cert_ocr_loading"
          >
            <n-upload-dragger class="paper_ocr_dragger">
              <template v-if="cert_ocr_loading">
                <n-spin size="medium" />
                <p style="margin: 8px 0 0; color: #666">AI 识别中，请稍候…</p>
              </template>
              <template v-else>
                <n-icon size="36" color="#409eff"><Scan /></n-icon>
                <p style="margin: 8px 0 4px; font-size: 15px; font-weight: 500">上传证书图片</p>
                <p style="margin: 0; color: #999; font-size: 13px">AI 按成果类型自动识别填写 · 支持 JPG / PNG</p>
              </template>
            </n-upload-dragger>
          </n-upload>
        </div>

        <!-- 基本信息区域 -->
        <div class="form_section">
          <h3 class="section_title">
            <FileText :size="20" />
            基本信息
          </h3>
          
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="学号" path="student_id">
                <n-input 
                  v-model:value="form_data.student_id" 
                  placeholder="请输入学号"
                  disabled
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <n-form-item label="姓名" path="name">
                <n-input 
                  v-model:value="form_data.name" 
                  placeholder="请输入姓名"
                  disabled
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="成果标题" path="title">
                <n-input 
                  v-model:value="form_data.title" 
                  placeholder="请输入成果标题"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <n-form-item label="成果类别" path="category">
                <n-select 
                  v-model:value="form_data.category" 
                  :options="category_opts" 
                  placeholder="请选择成果类别"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 详细信息区域 -->
        <div class="form_section">
          <h3 class="section_title">
            <Award :size="20" />
            详细信息
          </h3>
          
          <!-- 非专利：奖项 + 等级 -->
          <n-grid v-if="!is_patent" :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="奖项" path="award">
                <n-select
                  v-model:value="form_data.award"
                  :options="award_opts"
                  placeholder="请选择奖项"
                />
              </n-form-item>
            </n-grid-item>

            <n-grid-item>
              <n-form-item label="等级" path="level">
                <n-select
                  v-model:value="form_data.level"
                  :options="level_opts"
                  placeholder="请选择等级"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <!-- 专利类专属字段 -->
          <template v-if="is_patent">
            <n-grid :cols="2" :x-gap="24" :y-gap="16">
              <n-grid-item>
                <n-form-item label="专利类型">
                  <n-input
                    v-model:value="form_data.patent_type"
                    placeholder="如：发明专利 / 实用新型专利 / 软件著作权"
                    clearable
                  />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item label="专利号 / 登记号">
                  <n-input
                    v-model:value="form_data.patent_number"
                    placeholder="如：CN123456789B"
                    clearable
                  />
                </n-form-item>
              </n-grid-item>
            </n-grid>
            <n-grid :cols="2" :x-gap="24" :y-gap="16">
              <n-grid-item>
                <n-form-item label="发明人 / 著作权人">
                  <n-input
                    v-model:value="form_data.patent_inventors"
                    placeholder="多人用顿号分隔，如：张三、李四"
                    clearable
                  />
                </n-form-item>
              </n-grid-item>
              <n-grid-item>
                <n-form-item label="专利权人 / 著作权人单位">
                  <n-input
                    v-model:value="form_data.patent_holder"
                    placeholder="如：广西警察学院"
                    clearable
                  />
                </n-form-item>
              </n-grid-item>
            </n-grid>
          </template>

          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="获奖日期" path="date">
                <n-date-picker 
                  v-model:value="form_data.date" 
                  type="date" 
                  placeholder="选择获奖日期"
                  @update:value="handle_date_change"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <n-form-item label="导师所属学院" path="tutor_department">
                <n-select 
                  v-model:value="form_data.tutor_department" 
                  :options="department_opts" 
                  placeholder="请选择所属学院"
                  @update:value="handle_department_change"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>

          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="导师姓名" path="tutor_name">
                <n-select 
                  v-model:value="form_data.tutor_name" 
                  :options="filtered_teacher_opts" 
                  placeholder="请先选择学院，再选择导师"
                  :disabled="!form_data.tutor_department"
                  clearable
                  filterable
                />
              </n-form-item>
            </n-grid-item>
            
            <n-grid-item>
              <!-- 预留空位，保持布局平衡 -->
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 附件上传区域 -->
        <div class="form_section">
          <h3 class="section_title">
            <Upload :size="20" />
            附件上传
          </h3>
          
          <n-form-item label="相关文件" path="attachments">
            <n-upload
              v-model:file-list="form_data.attachments"
              multiple
              directory-dnd
              :max="5"
              list-type="text"
              @before-upload="before_upload"
              @remove="handle_file_remove"
            >
              <n-upload-dragger>
                <div style="margin-bottom: 12px">
                  <n-icon size="48" :depth="3">
                    <Upload />
                  </n-icon>
                </div>
                <n-text style="font-size: 16px">
                  点击或者拖动文件到该区域来上传
                </n-text>
                <n-p depth="3" style="margin: 8px 0 0 0">
                  支持上传证书、获奖证明、论文等相关文件，最多5个文件
                </n-p>
              </n-upload-dragger>
            </n-upload>
          </n-form-item>
        </div>

        <!-- 操作按钮 -->
        <div class="form_actions">
          <n-space justify="center" size="large">
            <n-button size="large" @click="reset_form">
              <template #icon><Refresh :size="20" /></template>
              重置表单
            </n-button>
            <n-button size="large" @click="save_draft">
              <template #icon><Save :size="20" /></template>
              保存草稿
            </n-button>
            <n-button type="primary" size="large" @click="submitAchievementForm" :loading="submitting">
              <template #icon><Send :size="20" /></template>
              提交成果
            </n-button>
          </n-space>
        </div>
      </n-form>
    </n-card>

    <!-- 论文表单 -->
    <n-card v-if="collect_type === 'paper'" class="form_card">
      <n-form
        ref="paper_form_ref"
        :model="paper_data"
        :rules="paper_rules"
        label-placement="top"
        require-mark-placement="right-hanging"
        size="medium"
      >
        <!-- OCR 快速识别 -->
        <div class="form_section ocr_hint_section">
          <h3 class="section_title"><Scan :size="20" />AI 快速识别（可选）</h3>
          <n-upload
            :custom-request="handle_paper_ocr"
            :show-file-list="false"
            accept=".jpg,.jpeg,.png"
            :disabled="paper_ocr_loading"
          >
            <n-upload-dragger class="paper_ocr_dragger">
              <template v-if="paper_ocr_loading">
                <n-spin size="medium" />
                <p style="margin: 8px 0 0; color: #666">AI 识别中，请稍候…</p>
              </template>
              <template v-else>
                <n-icon size="36" color="#409eff"><Scan /></n-icon>
                <p style="margin: 8px 0 4px; font-size: 15px; font-weight: 500">上传论文截图 / 录用通知图片</p>
                <p style="margin: 0; color: #999; font-size: 13px">AI 自动识别并填写下方信息 · 支持 JPG / PNG</p>
              </template>
            </n-upload-dragger>
          </n-upload>
        </div>

        <!-- 基本信息 -->
        <div class="form_section">
          <h3 class="section_title"><FileText :size="20" />基本信息</h3>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="学号" path="student_id">
                <n-input v-model:value="paper_data.student_id" disabled />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="姓名" path="name">
                <n-input v-model:value="paper_data.name" disabled />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 论文信息 -->
        <div class="form_section">
          <h3 class="section_title"><Award :size="20" />论文信息</h3>
          <n-grid :cols="1" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="论文题目" path="paper_title">
                <n-input v-model:value="paper_data.paper_title" placeholder="请输入完整论文题目" clearable />
              </n-form-item>
            </n-grid-item>
            <n-grid-item v-if="paper_data.paper_title_cn">
              <n-form-item label="中文题目（AI翻译）">
                <n-input v-model:value="paper_data.paper_title_cn" placeholder="英文论文自动翻译的中文题目" clearable />
              </n-form-item>
            </n-grid-item>
          </n-grid>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="期刊 / 会议名称" path="journal_name">
                <n-input v-model:value="paper_data.journal_name" placeholder="请输入期刊或会议全称" clearable />
              </n-form-item>
            </n-grid-item>
            <n-grid-item v-if="paper_data.journal_name_cn">
              <n-form-item label="中文期刊名（AI翻译）">
                <n-input v-model:value="paper_data.journal_name_cn" placeholder="英文期刊自动翻译的中文名称" clearable />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="期刊级别" path="journal_level">
                <n-select v-model:value="paper_data.journal_level" :options="journal_level_opts" placeholder="请选择期刊级别" />
              </n-form-item>
            </n-grid-item>
          </n-grid>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="发表状态" path="publish_status">
                <n-select v-model:value="paper_data.publish_status" :options="publish_status_opts" placeholder="请选择发表状态" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="发表 / 录用时间" path="publish_date">
                <n-date-picker
                  v-model:value="paper_data.publish_date"
                  type="date"
                  placeholder="选择日期"
                  clearable
                  style="width: 100%"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="作者排序" path="author_order">
                <n-select v-model:value="paper_data.author_order" :options="author_order_opts" placeholder="请选择作者排序" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="DOI（选填）" path="doi">
                <n-input v-model:value="paper_data.doi" placeholder="如 10.1016/j.xxx.2024.01.001" clearable />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 导师信息 -->
        <div class="form_section">
          <h3 class="section_title"><FileText :size="20" />导师信息</h3>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="导师所属学院" path="tutor_department">
                <n-select
                  v-model:value="paper_data.tutor_department"
                  :options="department_opts"
                  placeholder="请选择所属学院"
                  @update:value="handle_paper_department_change"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="导师姓名" path="tutor_name">
                <n-select
                  v-model:value="paper_data.tutor_name"
                  :options="filtered_teacher_opts"
                  placeholder="请先选择学院，再选择导师"
                  :disabled="!paper_data.tutor_department"
                  clearable
                  filterable
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 附件上传 -->
        <div class="form_section">
          <h3 class="section_title"><Upload :size="20" />附件上传</h3>
          <n-form-item label="录用通知 / 发表页截图" path="attachments">
            <n-upload
              v-model:file-list="paper_data.attachments"
              multiple
              :max="5"
              list-type="text"
              @before-upload="before_upload"
            >
              <n-upload-dragger>
                <div style="margin-bottom: 12px">
                  <n-icon size="48" :depth="3"><Upload /></n-icon>
                </div>
                <n-text style="font-size: 16px">点击或拖动文件到此处上传</n-text>
                <n-p depth="3" style="margin: 8px 0 0 0">支持 PDF、图片、Word，最多 5 个文件</n-p>
              </n-upload-dragger>
            </n-upload>
          </n-form-item>
        </div>

        <!-- 诚信承诺 -->
        <div class="form_section integrity_section">
          <n-form-item path="integrity_pledge" :show-label="false">
            <n-checkbox v-model:checked="paper_data.integrity_pledge">
              <span class="integrity_text">本人承诺以上填写的论文信息真实有效，如有造假愿承担相应责任</span>
            </n-checkbox>
          </n-form-item>
        </div>

        <!-- 操作按钮 -->
        <div class="form_actions">
          <n-space justify="center" size="large">
            <n-button size="large" @click="reset_paper_form">
              <template #icon><Refresh :size="20" /></template>
              重置表单
            </n-button>
            <n-button type="primary" size="large" @click="submit_paper_form" :loading="submitting" :disabled="!paper_data.integrity_pledge">
              <template #icon><Send :size="20" /></template>
              提交论文成果
            </n-button>
          </n-space>
        </div>
      </n-form>
    </n-card>

    <!-- 专利表单 -->
    <n-card v-if="collect_type === 'patent'" class="form_card">
      <n-form
        ref="patent_form_ref"
        :model="patent_data"
        :rules="patent_rules"
        label-placement="top"
        require-mark-placement="right-hanging"
        size="medium"
      >
        <!-- OCR 快速识别 -->
        <div class="form_section ocr_hint_section">
          <h3 class="section_title"><Scan :size="20" />AI 快速识别（可选）</h3>
          <n-upload
            :custom-request="handle_patent_ocr"
            :show-file-list="false"
            accept=".jpg,.jpeg,.png"
            :disabled="patent_ocr_loading"
          >
            <n-upload-dragger class="paper_ocr_dragger">
              <template v-if="patent_ocr_loading">
                <n-spin size="medium" />
                <p style="margin: 8px 0 0; color: #666">AI 识别中，请稍候…</p>
              </template>
              <template v-else>
                <n-icon size="36" color="#409eff"><Scan /></n-icon>
                <p style="margin: 8px 0 4px; font-size: 15px; font-weight: 500">上传专利证书 / 受理通知书图片</p>
                <p style="margin: 0; color: #999; font-size: 13px">AI 自动识别并填写下方信息 · 支持 JPG / PNG</p>
              </template>
            </n-upload-dragger>
          </n-upload>
        </div>

        <!-- 基本信息 -->
        <div class="form_section">
          <h3 class="section_title"><FileText :size="20" />基本信息</h3>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="学号" path="student_id">
                <n-input v-model:value="patent_data.student_id" disabled />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="姓名" path="name">
                <n-input v-model:value="patent_data.name" disabled />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 专利信息 -->
        <div class="form_section">
          <h3 class="section_title"><Bulb :size="20" />专利信息</h3>
          <n-grid :cols="1" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="专利 / 著作权名称" path="patent_title">
                <n-input v-model:value="patent_data.patent_title" placeholder="请输入专利或软件著作权的完整名称" clearable />
              </n-form-item>
            </n-grid-item>
          </n-grid>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="专利类型" path="patent_type">
                <n-select v-model:value="patent_data.patent_type" :options="patent_type_opts" placeholder="请选择专利类型" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="专利号 / 登记号" path="patent_number">
                <n-input v-model:value="patent_data.patent_number" placeholder="如：CN123456789B、2024SR0123456" clearable />
              </n-form-item>
            </n-grid-item>
          </n-grid>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="专利状态" path="patent_status">
                <n-select v-model:value="patent_data.patent_status" :options="patent_status_opts" placeholder="请选择当前状态" />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="授权 / 登记日期" path="patent_date">
                <n-date-picker
                  v-model:value="patent_data.patent_date"
                  type="date"
                  placeholder="选择日期"
                  clearable
                  style="width: 100%"
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="发明人 / 著作权人" path="patent_inventors">
                <n-input v-model:value="patent_data.patent_inventors" placeholder="多人用顿号分隔，如：张三、李四" clearable />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="专利权人 / 著作权人单位" path="patent_holder">
                <n-input v-model:value="patent_data.patent_holder" placeholder="如：广西警察学院" clearable />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 导师信息 -->
        <div class="form_section">
          <h3 class="section_title"><FileText :size="20" />导师信息</h3>
          <n-grid :cols="2" :x-gap="24" :y-gap="16">
            <n-grid-item>
              <n-form-item label="导师所属学院" path="tutor_department">
                <n-select
                  v-model:value="patent_data.tutor_department"
                  :options="department_opts"
                  placeholder="请选择所属学院"
                  @update:value="handle_patent_department_change"
                  clearable
                />
              </n-form-item>
            </n-grid-item>
            <n-grid-item>
              <n-form-item label="导师姓名" path="tutor_name">
                <n-select
                  v-model:value="patent_data.tutor_name"
                  :options="filtered_teacher_opts"
                  placeholder="请先选择学院，再选择导师"
                  :disabled="!patent_data.tutor_department"
                  clearable
                  filterable
                />
              </n-form-item>
            </n-grid-item>
          </n-grid>
        </div>

        <!-- 附件上传 -->
        <div class="form_section">
          <h3 class="section_title"><Upload :size="20" />附件上传</h3>
          <n-form-item label="专利证书 / 受理通知书（选填）" path="attachments">
            <n-upload
              v-model:file-list="patent_data.attachments"
              multiple
              :max="5"
              list-type="text"
              @before-upload="before_upload"
            >
              <n-upload-dragger>
                <div style="margin-bottom: 12px">
                  <n-icon size="48" :depth="3"><Upload /></n-icon>
                </div>
                <n-text style="font-size: 16px">点击或拖动文件到此处上传</n-text>
                <n-p depth="3" style="margin: 8px 0 0 0">支持 PDF、图片、Word，最多 5 个文件</n-p>
              </n-upload-dragger>
            </n-upload>
          </n-form-item>
        </div>

        <!-- 诚信承诺 -->
        <div class="form_section integrity_section">
          <n-form-item path="integrity_pledge" :show-label="false">
            <n-checkbox v-model:checked="patent_data.integrity_pledge">
              <span class="integrity_text">本人承诺以上填写的专利信息真实有效，如有造假愿承担相应责任，包括成果积分清零并记入信用档案。</span>
            </n-checkbox>
          </n-form-item>
        </div>

        <!-- 操作按钮 -->
        <div class="form_actions">
          <n-space justify="center" size="large">
            <n-button size="large" @click="reset_patent_form">
              <template #icon><Refresh :size="20" /></template>
              重置表单
            </n-button>
            <n-button type="primary" size="large" @click="submit_patent_form" :loading="submitting" :disabled="!patent_data.integrity_pledge">
              <template #icon><Send :size="20" /></template>
              提交专利成果
            </n-button>
          </n-space>
        </div>
      </n-form>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage, useDialog } from 'naive-ui'
import type { FormInst, UploadFileInfo } from 'naive-ui'
import {
  IconFileText as FileText,
  IconAward as Award,
  IconUpload as Upload,
  IconRefresh as Refresh,
  IconDeviceFloppy as Save,
  IconSend as Send,
  IconArrowLeft as ArrowLeft,
  IconScan as Scan,
  IconBulb as Bulb
} from '@tabler/icons-vue'
import {
  submitAchievement,
  getTeachers,
  getStudentMe,
  recognizeCertificate,
  uploadFile
} from '@/api'

// === API 适配器 ===

// 1. 创建成果适配器
const createAchievement = async (payload: any): Promise<any> => {
  const d = payload.data
  // 从教师选项中查找选中导师的真实 ID
  const selectedTeacher = filtered_teacher_opts.value.find(
    t => t.value === d.tutor_name
  )
  const teacherId = selectedTeacher?.teacher_id
    ? Number(selectedTeacher.teacher_id)
    : null

  if (!teacherId) {
    throw new Error('请选择有效的导师')
  }

  // 转换数据格式
  return submitAchievement({
      teacher_id: teacherId,
      title: d.title,
      type: d.category || 'competition',
      content_json: { ...d },
      evidence_url: ''
  })
}

const router = useRouter()
const message = useMessage()
const dialog = useDialog()

// 当前选中的成果类型：null = 未选 | 'certificate' = 证书/竞赛 | 'paper' = 学术论文
const collect_type = ref<null | 'certificate' | 'paper' | 'patent'>(null)

// 表单引用
const form_ref = ref<FormInst | null>(null)
const paper_form_ref = ref<FormInst | null>(null)

// 提交状态
const submitting = ref(false)

// 论文 OCR 识别状态
const paper_ocr_loading = ref(false)
const cert_ocr_loading = ref(false)

// 表单数据
const form_data = ref({
  student_id: '',
  name: '',
  category: '1', // 成果类别，对应后端category字段，默认为竞赛类
  award: '', // 奖项，对应后端award字段
  date: null as number | null, // 获奖日期，对应后端date字段
  level: '',
  title: '',
  tutor_department: '', // 导师所属学院
  tutor_name: '', // 导师姓名
  attachments: [] as UploadFileInfo[],
  // 专利专属字段
  patent_number: '',     // 专利号
  patent_type: '',       // 专利类型（发明/实用新型/外观设计/软件著作权）
  patent_inventors: '',  // 发明人（逗号分隔）
  patent_holder: '',     // 专利权人
})

// 是否为专利类别
const is_patent = computed(() => form_data.value.category === '5')

// 表单验证规则
const form_rules = {
  student_id: [
    { required: true, message: '请输入学号', trigger: 'blur' },
    { 
      pattern: /^[0-9]+$/, 
      message: '学号只能包含数字', 
      trigger: 'blur' 
    }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 50, message: '姓名长度应在2-50字符之间', trigger: 'blur' }
  ],
  title: [
    { required: true, message: '请输入成果标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度应在2-100字符之间', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择成果类别', trigger: 'change' }
  ],
  award: [
    {
      required: true,
      trigger: 'change',
      validator: (_rule: any, value: string) => {
        if (is_patent.value) return true // 专利类别不要求奖项
        if (!value) return new Error('请选择奖项')
        return true
      }
    }
  ],
  level: [
    {
      required: true,
      trigger: 'change',
      validator: (_rule: any, value: string) => {
        if (is_patent.value) return true // 专利类别不要求等级
        if (!value) return new Error('请选择等级')
        return true
      }
    }
  ],
  date: [
    { 
      required: true, 
      message: '请选择获奖日期', 
      trigger: 'change',
      validator: (rule: any, value: number | null) => {
        if (!value) {
          return new Error('请选择获奖日期')
        }
        const selected_date = new Date(value)
        const today = new Date()
        if (selected_date > today) {
          return new Error('获奖日期不能晚于今天')
        }
        return true
      }
    }
  ],
  tutor_department: [
    { required: true, message: '请选择导师所属学院', trigger: 'change' }
  ],
  tutor_name: [
    { required: true, message: '请选择导师姓名', trigger: 'change' }
  ]
}

// ========== 论文表单数据 ==========
const paper_data = ref({
  student_id: '',
  name: '',
  paper_title: '',
  journal_name: '',
  journal_level: '',
  publish_status: '',
  publish_date: null as number | null,
  author_order: '',
  doi: '',
  issn: '',
  tutor_department: '',
  tutor_name: '',
  evidence_url: '',
  attachments: [] as UploadFileInfo[],
  integrity_pledge: false,
  // 英文论文中文映射
  paper_title_cn: '',
  journal_name_cn: '',
  authors_cn: [] as string[],
  first_author_cn: '',
  issuing_organization_cn: ''
})

const paper_rules = {
  paper_title: [{ required: true, message: '请输入论文题目', trigger: 'blur' }],
  journal_name: [{ required: true, message: '请输入期刊/会议名称', trigger: 'blur' }],
  journal_level: [{ required: true, message: '请选择期刊级别', trigger: 'change' }],
  publish_status: [{ required: true, message: '请选择发表状态', trigger: 'change' }],
  publish_date: [{
    required: true,
    trigger: 'change',
    validator: (_rule: any, value: number | null) => {
      if (!value) return new Error('请选择发表/录用时间')
      if (new Date(value) > new Date()) return new Error('日期不能晚于今天')
      return true
    }
  }],
  doi: [{
    trigger: 'blur',
    validator: (_rule: any, value: string) => {
      if (!value) return true // DOI 选填
      if (!/^10\.\d{4,}\/\S+$/.test(value)) return new Error('DOI 格式不正确，应以 10. 开头，如 10.1016/j.xxx.2024.01.001')
      return true
    }
  }],
  author_order: [{ required: true, message: '请选择作者排序', trigger: 'change' }],
  attachments: [{
    required: true,
    trigger: 'change',
    validator: (_rule: any, value: UploadFileInfo[]) => {
      if (!value || value.length === 0) return new Error('请上传至少一个证明文件（录用通知/发表页截图）')
      return true
    }
  }],
  tutor_department: [{ required: true, message: '请选择导师所属学院', trigger: 'change' }],
  tutor_name: [{ required: true, message: '请选择导师姓名', trigger: 'change' }],
  integrity_pledge: [{
    required: true,
    trigger: 'change',
    validator: (_rule: any, value: boolean) => {
      if (!value) return new Error('请勾选诚信承诺')
      return true
    }
  }]
}

const journal_level_opts = [
  { label: 'SCI', value: 'SCI' },
  { label: 'EI', value: 'EI' },
  { label: '北大核心', value: '北大核心' },
  { label: '南大核心（CSSCI）', value: 'CSSCI' },
  { label: '普通期刊', value: '普通期刊' },
  { label: '会议论文', value: '会议论文' }
]

const publish_status_opts = [
  { label: '已发表', value: 'published' },
  { label: '录用待刊', value: 'accepted' },
  { label: '在审中', value: 'under_review' }
]

const author_order_opts = [
  { label: '第一作者', value: '第一作者' },
  { label: '通讯作者', value: '通讯作者' },
  { label: '第二作者', value: '第二作者' },
  { label: '第三作者及以后', value: '其他作者' }
]

// ========== 专利表单数据 ==========
const patent_form_ref = ref<FormInst | null>(null)
const patent_ocr_loading = ref(false)

const patent_data = ref({
  student_id: '',
  name: '',
  patent_title: '',
  patent_type: '',
  patent_number: '',
  patent_status: '',
  patent_date: null as number | null,
  patent_inventors: '',
  patent_holder: '',
  tutor_department: '',
  tutor_name: '',
  evidence_url: '',
  attachments: [] as UploadFileInfo[],
  integrity_pledge: false
})

const patent_rules = {
  patent_title: [{ required: true, message: '请输入专利/著作权名称', trigger: 'blur' }],
  patent_type: [{ required: true, message: '请选择专利类型', trigger: 'change' }],
  patent_number: [{ required: true, message: '请输入专利号/登记号', trigger: 'blur' }],
  patent_status: [{ required: true, message: '请选择专利状态', trigger: 'change' }],
  patent_date: [{
    required: true,
    trigger: 'change',
    validator: (_rule: any, value: number | null) => {
      if (!value) return new Error('请选择授权/登记日期')
      if (new Date(value) > new Date()) return new Error('日期不能晚于今天')
      return true
    }
  }],
  patent_inventors: [{ required: true, message: '请输入发明人/著作权人', trigger: 'blur' }],
  tutor_department: [{ required: true, message: '请选择导师所属学院', trigger: 'change' }],
  tutor_name: [{ required: true, message: '请选择导师姓名', trigger: 'change' }]
}

const patent_type_opts = [
  { label: '发明专利', value: '发明专利' },
  { label: '实用新型专利', value: '实用新型专利' },
  { label: '外观设计专利', value: '外观设计专利' },
  { label: '软件著作权', value: '软件著作权' }
]

const patent_status_opts = [
  { label: '已授权', value: 'granted' },
  { label: '已受理', value: 'accepted' },
  { label: '实审中', value: 'under_review' },
  { label: '已公开', value: 'published' }
]

// 选项配置 - 保留数字值，映射为后端字段值
const category_opts = [
  { label: '竞赛类', value: '1', backendValue: 'competition' },
  { label: '科研类', value: '2', backendValue: 'research' },
  { label: '项目类', value: '3', backendValue: 'project' },
  { label: '论文类', value: '4', backendValue: 'paper' },
  { label: '专利类', value: '5', backendValue: 'patent' },
  { label: '证书类', value: '6', backendValue: 'certification' }
]

// 修正奖项配置，确保标签与值匹配
const award_opts = [
  { label: '特等奖', value: 'grandprize' },
  { label: '一等奖', value: 'firstprize' },
  { label: '二等奖', value: 'secondprize' },
  { label: '三等奖', value: 'thirdprize' },
  { label: '优秀奖', value: 'honorablemention' },
]

const level_opts = [
  { label: '国家级', value: 'international' },
  { label: '省部级', value: 'provincial' },
  { label: '校级', value: 'university' },
  { label: '院级', value: 'college' }
]

// 学院选项配置 - 改为响应式，支持从后端动态获取
const department_opts = ref([
  { label: '计算机学院', value: '计算机学院' },
  { label: '软件学院', value: '软件学院' },
  { label: '人工智能学院', value: '人工智能学院' }
])

// 教师数据管理
const teachers_data = ref<any[]>([])
const current_department_teachers = ref<any[]>([])
const loading_teachers = ref(false)

// 根据当前学院的教师数据生成选项
const filtered_teacher_opts = computed(() => {
  // 任意一个表单选择了学院且有教师数据即可显示
  const hasDept = form_data.value.tutor_department ||
                  paper_data.value.tutor_department ||
                  patent_data.value.tutor_department
  if (!hasDept || current_department_teachers.value.length === 0) {
    return []
  }

  return current_department_teachers.value.map(teacher => ({
    label: teacher.name || '未知教师',
    value: teacher.name || '',
    teacher_id: teacher.id
  }))
})

// 允许的文件类型配置
const allowed_file_types = {
  'application/pdf': 'PDF文件',
  'image/jpeg': 'JPEG图片',
  'image/jpg': 'JPG图片',
  'image/png': 'PNG图片',
  'application/msword': 'Word文档',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'Word文档',
  'application/vnd.ms-excel': 'Excel文档',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'Excel文档'
}

// 最大文件大小（10MB）
const MAX_FILE_SIZE = 10 * 1024 * 1024

// 方法
const go_back = () => {
  if (collect_type.value) {
    collect_type.value = null
  } else {
    router.push('/student/achievement')
  }
}

const handle_paper_department_change = async (value: string) => {
  paper_data.value.tutor_name = ''
  if (value) await fetch_teachers_by_department(value)
}

const reset_paper_form = () => {
  paper_form_ref.value?.restoreValidation()
  const { student_id, name } = paper_data.value
  Object.assign(paper_data.value, {
    student_id, name,
    paper_title: '', journal_name: '', journal_level: '',
    publish_status: '', publish_date: null, author_order: '',
    doi: '', tutor_department: '', tutor_name: '', attachments: [],
    integrity_pledge: false,
    paper_title_cn: '', journal_name_cn: '', authors_cn: [],
    first_author_cn: '', issuing_organization_cn: ''
  })
  message.success('表单已重置')
}

// ========== 论文表单内嵌 OCR ==========
const handle_paper_ocr = async ({ file, onFinish, onError }: any) => {
  if (!file.file) { onError(); return }
  paper_ocr_loading.value = true
  try {
    const res = await recognizeCertificate(file.file, 'paper')
    const raw = res?.recognized_data

    if (!raw) {
      message.error('识别失败，请手动填写或更换图片')
      onError()
      return
    }

    if (raw.document_type === 'certificate') {
      message.warning('检测到证书类文件，请确认图片是否为论文截图/录用通知')
    }

    const publishStatusMap: Record<string, string> = {
      '已发表': 'published',
      '录用待刊': 'accepted',
      '在审中': 'under_review'
    }

    if (raw.paper_title)   paper_data.value.paper_title   = raw.paper_title
    if (raw.journal_name)  paper_data.value.journal_name  = raw.journal_name
    if (raw.journal_level) paper_data.value.journal_level = raw.journal_level
    if (raw.publish_status) paper_data.value.publish_status = publishStatusMap[raw.publish_status] || raw.publish_status
    if (raw.author_order) {
      const valid_orders = ['第一作者', '通讯作者', '第二作者', '其他作者']
      if (valid_orders.includes(raw.author_order)) {
        paper_data.value.author_order = raw.author_order
      } else {
        paper_data.value.author_order = ''
      }
    }
    if (raw.doi)           paper_data.value.doi           = raw.doi
    if (raw.issn)          paper_data.value.issn          = raw.issn
    if (res.file_url)      paper_data.value.evidence_url  = res.file_url
    // 英文论文中文映射
    if (raw.paper_title_cn)   paper_data.value.paper_title_cn   = raw.paper_title_cn
    if (raw.journal_name_cn)  paper_data.value.journal_name_cn  = raw.journal_name_cn
    if (raw.authors_cn)       paper_data.value.authors_cn       = raw.authors_cn
    if (raw.first_author_cn)  paper_data.value.first_author_cn  = raw.first_author_cn
    if (raw.issuing_organization_cn) paper_data.value.issuing_organization_cn = raw.issuing_organization_cn

    if (raw.publish_date) {
      const d = new Date(raw.publish_date)
      if (!isNaN(d.getTime())) paper_data.value.publish_date = d.getTime()
    }

    message.success('识别完成，请核对信息并补充导师')
    onFinish()
  } catch (e: any) {
    const errorMsg = e.message || 'OCR 识别出错';
    if (errorMsg.includes('上传的图片类型不符合') || errorMsg.includes('上传的图片类型与当前选择的成果类别不匹配')) {
      dialog.warning({
        title: '类型不匹配',
        content: errorMsg,
        positiveText: '退出',
        onPositiveClick: () => {
          collect_type.value = null; // 返回类型选择页面
        }
      });
    } else {
      message.error(errorMsg)
    }
    onError()
  } finally {
    paper_ocr_loading.value = false
  }
}

// ========== 证书表单 OCR（按成果类型路由） ==========
const handle_cert_ocr = async ({ file, onFinish, onError }: any) => {
  if (!file.file) { onError(); return }

  // 将前端 category value 映射到后端 cert_type
  const categoryBackendMap: Record<string, string> = {
    '1': 'competition',
    '2': 'research',
    '3': 'project',
    '5': 'patent',
    '6': 'certificate',
  }
  const certType = categoryBackendMap[form_data.value.category] || 'certificate'

  cert_ocr_loading.value = true
  try {
    const res = await recognizeCertificate(file.file, certType)
    const raw = res?.recognized_data

    if (!raw) {
      message.error('识别失败，请手动填写或更换图片')
      onError()
      return
    }

    // 通用字段填充
    if (raw.title)    form_data.value.title = raw.title
    if (raw.issue_date || raw.date) {
      const dateStr = (raw.issue_date || raw.date) as string
      const d = new Date(dateStr)
      if (!isNaN(d.getTime())) form_data.value.date = d.getTime()
    }

    if (certType === 'patent') {
      // 专利专属字段映射
      form_data.value.patent_type      = (raw.patent_type || raw.award || '') as string
      form_data.value.patent_number    = (raw.patent_number || raw.certificate_number || '') as string
      form_data.value.patent_inventors = Array.isArray(raw.team_members) && raw.team_members.length
        ? (raw.team_members as string[]).join('、')
        : ((raw.recipient_name || '') as string)
      form_data.value.patent_holder    = (raw.patent_holder || '') as string
    } else {
      // 非专利：填充奖项和等级
      if (raw.award) form_data.value.award = raw.award
      if (raw.award_level) {
        const levelMap: Record<string, string> = {
          '国家级': '国家级', '省部级': '省部级', '校级': '校级', '院级': '院级'
        }
        const matched = Object.keys(levelMap).find(k => (raw.award_level || '').includes(k))
        if (matched) form_data.value.level = levelMap[matched]
      }
    }

    // 类型专属提示
    const typeHints: Record<string, string> = {
      competition: `竞赛识别完成：${raw.certificate_name || ''}${raw.award ? ' · ' + raw.award : ''}`,
      patent: `专利识别完成：${raw.patent_name || raw.certificate_name || ''}（${form_data.value.patent_type}）`,
      research: `科研成果识别完成：${raw.achievement_name || raw.certificate_name || ''}`,
      project: `项目识别完成：${raw.project_name || raw.certificate_name || ''}`,
      certificate: `证书识别完成：${raw.certificate_name || ''}`,
    }
    message.success((typeHints[certType] || '识别完成') + '，请核对信息')
    onFinish()
  } catch (e: any) {
    const errorMsg = e.message || 'OCR 识别出错';
    if (errorMsg.includes('上传的图片类型不符合') || errorMsg.includes('上传的图片类型与当前选择的成果类别不匹配')) {
      dialog.warning({
        title: '类型不匹配',
        content: errorMsg,
        positiveText: '退出',
        onPositiveClick: () => {
          collect_type.value = null; // 返回类型选择页面
        }
      });
    } else {
      message.error(errorMsg)
    }
    onError()
  } finally {
    cert_ocr_loading.value = false
  }
}

const submit_paper_form = async () => {
  try {
    await paper_form_ref.value?.validate()
    submitting.value = true

    const selectedTeacher = filtered_teacher_opts.value.find(
      t => t.value === paper_data.value.tutor_name
    )
    const teacherId = selectedTeacher?.teacher_id ? Number(selectedTeacher.teacher_id) : null
    if (!teacherId) throw new Error('请选择有效的导师')

    const publish_date_str = paper_data.value.publish_date
      ? (() => {
          const d = new Date(paper_data.value.publish_date!)
          return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
        })()
      : ''

    // 上传附件文件到服务器
    const uploaded_urls: string[] = []
    for (const fileInfo of paper_data.value.attachments) {
      if (fileInfo.file) {
        try {
          const res = await uploadFile(fileInfo.file)
          if (res && res.url) uploaded_urls.push(res.url)
        } catch (e) {
          console.error('文件上传失败:', fileInfo.name, e)
          throw new Error(`文件 "${fileInfo.name}" 上传失败，请重试`)
        }
      }
    }

    await submitAchievement({
      teacher_id: teacherId,
      title: paper_data.value.paper_title_cn || paper_data.value.paper_title,
      type: 'paper',
      content_json: {
        paper_title: paper_data.value.paper_title,
        journal_name: paper_data.value.journal_name,
        journal_level: paper_data.value.journal_level,
        publish_status: paper_data.value.publish_status,
        publish_date: publish_date_str,
        author_order: paper_data.value.author_order,
        doi: paper_data.value.doi,
        issn: paper_data.value.issn,
        tutor_department: paper_data.value.tutor_department,
        tutor_name: paper_data.value.tutor_name,
        attachment_urls: uploaded_urls,
        // 英文论文中文映射（用于中文搜索）
        ...(paper_data.value.paper_title_cn ? { paper_title_cn: paper_data.value.paper_title_cn } : {}),
        ...(paper_data.value.journal_name_cn ? { journal_name_cn: paper_data.value.journal_name_cn } : {}),
        ...(paper_data.value.authors_cn?.length ? { authors_cn: paper_data.value.authors_cn } : {}),
        ...(paper_data.value.first_author_cn ? { first_author_cn: paper_data.value.first_author_cn } : {}),
        ...(paper_data.value.issuing_organization_cn ? { issuing_organization_cn: paper_data.value.issuing_organization_cn } : {})
      },
      evidence_url: paper_data.value.evidence_url || uploaded_urls[0] || ''
    })

    message.success('论文成果提交成功！')
    router.push('/student/achievement')
  } catch (error: any) {
    if (error.name === 'ValidationError') {
      message.error('请完善必填信息后再提交')
    } else {
      message.error(error.message || '提交失败，请重试')
    }
  } finally {
    submitting.value = false
  }
}

// ========== 专利表单方法 ==========
const handle_patent_department_change = async (value: string) => {
  patent_data.value.tutor_name = ''
  if (value) await fetch_teachers_by_department(value)
}

const reset_patent_form = () => {
  patent_form_ref.value?.restoreValidation()
  const { student_id, name } = patent_data.value
  Object.assign(patent_data.value, {
    student_id, name,
    patent_title: '', patent_type: '', patent_number: '',
    patent_status: '', patent_date: null, patent_inventors: '',
    patent_holder: '', tutor_department: '', tutor_name: '',
    evidence_url: '', attachments: []
  })
  message.success('表单已重置')
}

const submit_patent_form = async () => {
  try {
    await patent_form_ref.value?.validate()
    submitting.value = true

    const selectedTeacher = filtered_teacher_opts.value.find(
      t => t.value === patent_data.value.tutor_name
    )
    const teacherId = selectedTeacher?.teacher_id ? Number(selectedTeacher.teacher_id) : null
    if (!teacherId) throw new Error('请选择有效的导师')

    const patent_date_str = patent_data.value.patent_date
      ? (() => {
          const d = new Date(patent_data.value.patent_date!)
          return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
        })()
      : ''

    // 上传附件文件到服务器
    const uploaded_urls: string[] = []
    for (const fileInfo of patent_data.value.attachments) {
      if (fileInfo.file) {
        try {
          const res = await uploadFile(fileInfo.file)
          if (res && res.url) uploaded_urls.push(res.url)
        } catch (e) {
          console.error('文件上传失败:', fileInfo.name, e)
          throw new Error(`文件 "${fileInfo.name}" 上传失败，请重试`)
        }
      }
    }

    await submitAchievement({
      teacher_id: teacherId,
      title: patent_data.value.patent_title,
      type: 'patent',
      content_json: {
        patent_title: patent_data.value.patent_title,
        patent_type: patent_data.value.patent_type,
        patent_number: patent_data.value.patent_number,
        patent_status: patent_data.value.patent_status,
        patent_date: patent_date_str,
        patent_inventors: patent_data.value.patent_inventors,
        patent_holder: patent_data.value.patent_holder,
        tutor_department: patent_data.value.tutor_department,
        tutor_name: patent_data.value.tutor_name,
        attachment_urls: uploaded_urls
      },
      evidence_url: patent_data.value.evidence_url || uploaded_urls[0] || ''
    })

    message.success('专利成果提交成功！')
    router.push('/student/achievement')
  } catch (error: any) {
    if (error.name === 'ValidationError') {
      message.error('请完善必填信息后再提交')
    } else {
      message.error(error.message || '提交失败，请重试')
    }
  } finally {
    submitting.value = false
  }
}

const handle_patent_ocr = async ({ file, onFinish, onError }: any) => {
  if (!file.file) { onError(); return }
  patent_ocr_loading.value = true
  try {
    const res = await recognizeCertificate(file.file, 'patent')
    const raw = res?.recognized_data

    if (!raw) {
      message.error('识别失败，请手动填写或更换图片')
      onError()
      return
    }

    if (raw.title || raw.patent_name || raw.certificate_name)
      patent_data.value.patent_title = (raw.title || raw.patent_name || raw.certificate_name) as string
    if (raw.patent_type || raw.award)
      patent_data.value.patent_type = (raw.patent_type || raw.award) as string
    if (raw.patent_number || raw.certificate_number)
      patent_data.value.patent_number = (raw.patent_number || raw.certificate_number) as string
    if (raw.patent_holder)
      patent_data.value.patent_holder = raw.patent_holder as string
    if (Array.isArray(raw.team_members) && raw.team_members.length) {
      patent_data.value.patent_inventors = (raw.team_members as string[]).join('、')
    } else if (raw.recipient_name) {
      patent_data.value.patent_inventors = raw.recipient_name as string
    }
    if (raw.issue_date || raw.date) {
      const d = new Date((raw.issue_date || raw.date) as string)
      if (!isNaN(d.getTime())) patent_data.value.patent_date = d.getTime()
    }
    if (res.file_url) patent_data.value.evidence_url = res.file_url

    message.success('专利识别完成，请核对信息并补充导师')
    onFinish()
  } catch (e: any) {
    const errorMsg = e.message || 'OCR 识别出错';
    if (errorMsg.includes('上传的图片类型不符合') || errorMsg.includes('上传的图片类型与当前选择的成果类别不匹配')) {
      dialog.warning({
        title: '类型不匹配',
        content: errorMsg,
        positiveText: '退出',
        onPositiveClick: () => {
          collect_type.value = null; // 返回类型选择页面
        }
      });
    } else {
      message.error(errorMsg)
    }
    onError()
  } finally {
    patent_ocr_loading.value = false
  }
}

const handle_date_change = (value: number | null) => {
  // 日期变化时无需额外处理，直接使用 date
  console.log('日期已更新:', value ? new Date(value).toLocaleDateString() : '未选择')
}

// 处理学院变化
const handle_department_change = async (value: string) => {
  // 清空导师选择
  form_data.value.tutor_name = ''
  console.log('学院已更新:', value)
  
  // 根据选择的学院获取对应的教师信息
  if (value) {
    await fetch_teachers_by_department(value)
  }
}

// 获取所有教师数据（初始化时使用）
const fetch_teachers_data = async () => {
  if (loading_teachers.value) return
  try {
    loading_teachers.value = true
    const allTeachers = await getTeachers() as any[]
    teachers_data.value = allTeachers.map((item: any) => ({
      id: item.id?.toString() || '',
      name: item.name || '',
      title: item.title || '',
      department: item.department || item.college || ''
    }))
  } catch (error: any) {
    console.error('获取教师数据失败:', error)
  } finally {
    loading_teachers.value = false
  }
}

// 根据学院获取教师数据
const fetch_teachers_by_department = async (department: string) => {
  try {
    loading_teachers.value = true
    // getTeachers() 经过响应拦截器后直接返回教师数组
    const allTeachers = await getTeachers() as any[]

    // 按学院名称过滤
    const filtered = allTeachers.filter((t: any) => {
      const dept = t.department || t.college || ''
      return dept === department || dept.includes(department) || department.includes(dept)
    })

    current_department_teachers.value = filtered.map((item: any) => ({
      id: item.id?.toString() || '',
      name: item.name || '',
      title: item.title || '',
      department: item.department || item.college || department
    }))

    if (current_department_teachers.value.length > 0) {
      message.success(`成功加载 ${current_department_teachers.value.length} 位${department}教师信息`)
    } else {
      message.warning(`${department}暂无教师数据`)
    }
  } catch (error: any) {
    console.error(`获取${department}教师数据失败:`, error)
    message.error(`获取教师信息失败，请检查网络连接`)
    current_department_teachers.value = []
  } finally {
    loading_teachers.value = false
  }
}

const before_upload = (data: { file: UploadFileInfo }) => {
  const file = data.file
  
  // 检查文件类型
  if (!file.type || !allowed_file_types[file.type as keyof typeof allowed_file_types]) {
    const allowed_types = Object.values(allowed_file_types).join('、')
    message.error(`只支持以下文件类型：${allowed_types}`)
    return false
  }
  
  // 检查文件大小
  if ((file.file?.size || 0) > MAX_FILE_SIZE) {
    message.error('文件大小不能超过10MB')
    return false
  }
  
  // 检查文件名长度
  if (file.name && file.name.length > 100) {
    message.error('文件名长度不能超过100个字符')
    return false
  }
  
  // 检查是否有重复文件
  const existing_files = form_data.value.attachments
  const is_duplicate = existing_files.some(existing_file => 
    existing_file.name === file.name && existing_file.file?.size === file.file?.size
  )
  
  if (is_duplicate) {
    message.warning('该文件已存在，请勿重复上传')
    return false
  }
  
  return true
}

const handle_file_remove = (data: { file: UploadFileInfo }) => {
  message.info('文件已移除')
}

const reset_form = () => {
  form_ref.value?.restoreValidation()
  Object.assign(form_data.value, {
    student_id: '',
    name: '',
    category: '1', // 默认为竞赛类
    award: '',
    date: null,
    level: '',
    title: '',
    tutor_department: '',
    tutor_name: '',
    attachments: [],
    patent_number: '',
    patent_type: '',
    patent_inventors: '',
    patent_holder: '',
  })
  message.success('表单已重置')
}

const save_draft = () => {
  try {
    const draft_data = { ...form_data.value }
    // 不保存文件对象，只保存文件信息
    draft_data.attachments = draft_data.attachments.map(file => ({
      ...file,
      file: null // 清除文件对象，避免序列化问题
    }))
    
    localStorage.setItem('achievement_draft', JSON.stringify(draft_data))
    message.success('草稿已保存')
  } catch (error) {
    console.error('保存草稿失败:', error)
    message.error('保存草稿失败，请重试')
  }
}

// 主要提交函数
const submitAchievementForm = async () => {
  try {
    // 表单验证
    await form_ref.value?.validate()
    submitting.value = true
    
    // 获取当前选择的 category 数字值
    const selectedCategory = form_data.value.category;
    
    // 找到对应的后端字段值
    const selectedCategoryOption = category_opts.find(option => option.value === selectedCategory);
    const categoryBackendValue = selectedCategoryOption ? selectedCategoryOption.backendValue : '';

    // 构建符合后端API要求的提交数据格式
    const dateStr = form_data.value.date ? (() => {
      const d = new Date(form_data.value.date)
      const yyyy = d.getFullYear()
      const mm = String(d.getMonth() + 1).padStart(2, '0')
      const dd = String(d.getDate()).padStart(2, '0')
      return `${yyyy}-${mm}-${dd}`
    })() : ''

    const submit_data = {
      data: {
        student_id: form_data.value.student_id.trim(),
        name: form_data.value.name.trim(),
        category: categoryBackendValue,  // 使用映射后的值
        award: is_patent.value ? form_data.value.patent_type : form_data.value.award,
        level: form_data.value.level,
        date: dateStr,
        title: form_data.value.title.trim(),
        tutor_department: form_data.value.tutor_department,
        tutor_name: form_data.value.tutor_name,
        // 专利专属字段（category 为 patent 时有值）
        ...(is_patent.value ? {
          patent_number: form_data.value.patent_number,
          patent_inventors: form_data.value.patent_inventors,
          patent_holder: form_data.value.patent_holder,
        } : {})
      }
    }
    
    // 上传附件文件到服务器
    const uploaded_urls: string[] = []
    for (const fileInfo of form_data.value.attachments) {
      if (fileInfo.file) {
        try {
          const res = await uploadFile(fileInfo.file)
          if (res && res.url) uploaded_urls.push(res.url)
        } catch (e) {
          console.error('文件上传失败:', fileInfo.name, e)
          throw new Error(`文件 "${fileInfo.name}" 上传失败，请重试`)
        }
      }
    }
    if (uploaded_urls.length > 0) {
      (submit_data.data as any).attachment_urls = uploaded_urls;
      (submit_data.data as any).evidence_url = uploaded_urls[0]
    }

    console.log('提交数据:', submit_data)

    // 调用API提交到 /api/achievements
    const response = await createAchievement(submit_data)
    
    // 注意：响应拦截器已经返回了 response.data，所以这里的 response 就是数据本身
    // 只要没抛出异常就是成功
    console.log('提交成功，响应数据:', response)
    message.success('成果提交成功！')
    // 清除草稿
    localStorage.removeItem('achievement_draft')
    // 返回成果展示页面
    router.push('/student/achievement')
    
  } catch (error: any) {
    console.error('提交失败:', error)
    
    // 详细的错误处理
    if (error.name === 'ValidationError') {
      message.error('请完善必填信息后再提交')
    } else if (error.response?.status === 400) {
      message.error('数据格式有误，请检查后重试')
    } else if (error.response?.status === 401) {
      message.error('身份验证失败，请重新登录')
    } else if (error.response?.status === 403) {
      message.error('权限不足，无法提交成果')
    } else if (error.response?.status === 500) {
      message.error('服务器错误，请稍后重试')
    } else if (error.message?.includes('网络')) {
      message.error('网络连接异常，请检查网络后重试')
    } else {
      message.error('提交失败，请重试或联系管理员')
    }
  } finally {
    submitting.value = false
  }
}


// 动态获取学院列表
const init_departments = async () => {
  try {
    const teachers = await getTeachers() as any[]
    const depts = new Set<string>()
    teachers.forEach((t: any) => {
      const dept = t.department || t.college
      if (dept) depts.add(dept)
    })
    if (depts.size > 0) {
      department_opts.value = Array.from(depts).map(d => ({ label: d, value: d }))
    }
  } catch (error) {
    console.error('同步学院列表失败，使用默认值:', error)
  }
}

// 自动填入当前登录学生的信息
const loadCurrentStudentInfo = async () => {
  try {
    const studentInfo = await getStudentMe()
    if (studentInfo) {
      form_data.value.student_id = studentInfo.student_id || ''
      form_data.value.name = studentInfo.name || ''
      paper_data.value.student_id = studentInfo.student_id || ''
      paper_data.value.name = studentInfo.name || ''
      patent_data.value.student_id = studentInfo.student_id || ''
      patent_data.value.name = studentInfo.name || ''
      console.log('已自动填入学生信息:', { student_id: studentInfo.student_id, name: studentInfo.name })
    }
  } catch (error) {
    console.warn('获取当前学生信息失败，尝试从本地读取:', error)
    // 回退：从 localStorage 读取登录时存储的 userInfo
    try {
      const userInfoStr = localStorage.getItem('userInfo')
      if (userInfoStr) {
        const userInfo = JSON.parse(userInfoStr)
        form_data.value.student_id = userInfo.student_id || ''
        form_data.value.name = userInfo.name || ''
        paper_data.value.student_id = userInfo.student_id || ''
        paper_data.value.name = userInfo.name || ''
        console.log('已从本地存储填入学生信息')
      }
    } catch (e) {
      console.error('从本地存储读取用户信息失败:', e)
    }
  }
}

// 页面初始化
onMounted(() => {
  // 1. 同步学院数据
  init_departments()

  // 2. 自动填入当前登录学生的信息
  loadCurrentStudentInfo()

  // 3. 检查是否有来自 OCR 的论文识别数据（两阶段OCR: paper路径）
  try {
    const ocrPaperStr = localStorage.getItem('ocr_paper_data')
    if (ocrPaperStr) {
      localStorage.removeItem('ocr_paper_data')
      const ocrData = JSON.parse(ocrPaperStr)
      collect_type.value = 'paper'

      const publishStatusMap: Record<string, string> = {
        '已发表': 'published',
        '录用待刊': 'accepted',
        '在审中': 'under_review'
      }

      paper_data.value.paper_title = ocrData.paper_title || ''
      paper_data.value.journal_name = ocrData.journal_name || ''
      paper_data.value.journal_level = ocrData.journal_level || ''
      paper_data.value.publish_status = publishStatusMap[ocrData.publish_status] || ''
      paper_data.value.author_order = ocrData.author_order || ''
      paper_data.value.doi = ocrData.doi || ''
      paper_data.value.evidence_url = ocrData.evidence_url || ''
      // 英文论文中文映射
      paper_data.value.paper_title_cn = ocrData.paper_title_cn || ''
      paper_data.value.journal_name_cn = ocrData.journal_name_cn || ''
      paper_data.value.authors_cn = ocrData.authors_cn || []
      paper_data.value.first_author_cn = ocrData.first_author_cn || ''
      paper_data.value.issuing_organization_cn = ocrData.issuing_organization_cn || ''

      if (ocrData.publish_date) {
        const d = new Date(ocrData.publish_date)
        if (!isNaN(d.getTime())) {
          paper_data.value.publish_date = d.getTime()
        }
      }

      message.success('已自动填入论文OCR识别信息，请核对内容并补充导师信息')
      console.log('✅ 已从OCR预填论文数据:', ocrData)
    }
  } catch (e) {
    console.error('读取OCR论文数据失败:', e)
  }

  // 页面初始化，不再预加载所有教师数据
  // 教师数据将在用户选择学院时按需加载
  
  // 尝试恢复草稿
  try {
    const draft = localStorage.getItem('achievement_draft')
    if (draft) {
      const draft_data = JSON.parse(draft)
      // 恢复基本数据，但不恢复文件列表（文件对象无法序列化）
      // 不覆盖已自动填入的 student_id 和 name
      const { student_id, name, ...otherDraftData } = draft_data
      Object.assign(form_data.value, {
        ...otherDraftData,
        attachments: [] // 重置文件列表
      })
      message.info('已恢复上次保存的草稿（不包含文件）')
    }
  } catch (error) {
    console.error('恢复草稿失败:', error)
    localStorage.removeItem('achievement_draft') // 清除损坏的草稿
  }
})
</script>

<style scoped>
.collect_page {
  padding: 16px;
  font-family: "Microsoft YaHei", sans-serif;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  margin-bottom: 24px;
  padding: 20px 0;
}

.header_top {
  margin-bottom: 16px;
}

.back_btn {
  color: #409eff;
  font-size: 14px;
  padding: 8px 12px;
  transition: all 0.3s ease;
}

.back_btn:hover {
  background-color: #f0f8ff;
  color: #337ecc;
}

.header h1 {
  font-weight: 700;
  font-size: 28px;
  margin: 0;
  color: #333;
}

.header p {
  color: #666;
  font-size: 16px;
  margin: 8px 0 0 0;
}

.form_card {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form_section {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.form_section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.section_title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 20px 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.ocr_hint_section {
  background: #f0f7ff;
  border-radius: 8px;
  padding: 16px 20px 20px;
  border: 1px dashed #91caff;
}

.paper_ocr_dragger {
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 20px;
  background: #fff;
  border-radius: 6px;
}

.integrity_section {
  margin-top: 24px;
  padding: 16px 20px;
  background: #fffbe6;
  border: 1px solid #ffe58f;
  border-radius: 8px;
}

.integrity_text {
  font-size: 13px;
  color: #614700;
  line-height: 1.6;
}

.form_actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .collect_page {
    padding: 12px;
  }
  
  .form_section {
    margin-bottom: 24px;
  }
  
  .section_title {
    font-size: 14px;
  }
  
  /* 移动端表单布局调整 */
  :deep(.n-grid) {
    grid-template-columns: 1fr !important;
  }
}

/* 文件上传样式优化 */
:deep(.n-upload-dragger) {
  border: 2px dashed #d9d9d9;
  border-radius: 6px;
  background-color: #fafafa;
  transition: all 0.3s ease;
}

:deep(.n-upload-dragger:hover) {
  border-color: #409eff;
  background-color: #f0f8ff;
}

/* 表单项间距优化 */
:deep(.n-form-item) {
  margin-bottom: 0;
}

/* 按钮样式优化 */
:deep(.n-button) {
  border-radius: 6px;
}

/* 输入框样式优化 */
:deep(.n-input) {
  border-radius: 6px;
}

:deep(.n-select) {
  border-radius: 6px;
}

:deep(.n-date-picker) {
  width: 100%;
}
/* ========== 类型选择 ========== */
.type_select {
  max-width: 1200px;
  margin: 0 auto;
}

.type_grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.type_card {
  background: #fff;
  border: 2px solid #e8eaf6;
  border-radius: 12px;
  padding: 40px 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.25s ease;
}

.type_card:hover {
  border-color: #409eff;
  box-shadow: 0 8px 24px rgba(64, 158, 255, 0.15);
  transform: translateY(-4px);
}

.type_icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 20px;
}

.certificate_icon {
  background: linear-gradient(135deg, #fff3e0, #ffe0b2);
  color: #f57c00;
}

.paper_icon {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  color: #1976d2;
}

.patent_icon {
  background: linear-gradient(135deg, #fff3e0, #ffe0b2);
  color: #e65100;
}

.type_title {
  font-size: 20px;
  font-weight: 700;
  color: #333;
  margin-bottom: 12px;
}

.type_desc {
  font-size: 14px;
  color: #888;
  line-height: 1.6;
  margin-bottom: 20px;
}

.type_action {
  font-size: 14px;
  color: #409eff;
  font-weight: 600;
}
</style>