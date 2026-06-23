(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  // --- Chart: Policy Count Comparison ---
  var chart1 = echarts.init(document.getElementById('chart-policy-count'), null, { renderer: 'svg' });
  chart1.setOption({
    animation: false,
    tooltip: { trigger: 'axis', appendToBody: true },
    legend: { data: ['国内', '国外'], bottom: 0, textStyle: { color: muted } },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '10%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['6月17日', '6月12日', '6月9日', '6月8日', '4月29日', '4月17日', '5月19日'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 11 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: rule, type: 'dashed' } },
      axisLabel: { color: muted }
    },
    series: [
      {
        name: '国内',
        type: 'bar',
        data: [1, 2, 1, 1, 1, 1, 1],
        itemStyle: { color: accent, borderRadius: [4, 4, 0, 0] },
        barWidth: '30%'
      },
      {
        name: '国外',
        type: 'bar',
        data: [0, 1, 0, 0, 0, 0, 0],
        itemStyle: { color: accent2, borderRadius: [4, 4, 0, 0] },
        barWidth: '30%'
      }
    ]
  });
  window.addEventListener('resize', function() { chart1.resize(); });

  // --- Chart: Hot Area Distribution ---
  var chart2 = echarts.init(document.getElementById('chart-hot-area'), null, { renderer: 'svg' });
  chart2.setOption({
    animation: false,
    tooltip: { trigger: 'item', appendToBody: true },
    legend: { bottom: 0, textStyle: { color: muted }, itemWidth: 12, itemHeight: 12 },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '45%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 6, borderColor: bg2, borderWidth: 2 },
      label: { show: true, color: ink, fontSize: 12, formatter: '{b}\n{d}%' },
      labelLine: { lineStyle: { color: rule } },
      data: [
        { value: 25, name: '城市更新', itemStyle: { color: accent } },
        { value: 20, name: '数字治理', itemStyle: { color: accent2 } },
        { value: 18, name: 'AI应用', itemStyle: { color: muted } },
        { value: 15, name: '数字孪生', itemStyle: { color: accent + 'cc' } },
        { value: 12, name: '智能出行', itemStyle: { color: accent2 + 'cc' } },
        { value: 10, name: '数据要素', itemStyle: { color: muted + 'cc' } }
      ]
    }]
  });
  window.addEventListener('resize', function() { chart2.resize(); });

  // --- Chart: Policy Level Distribution ---
  var chart3 = echarts.init(document.getElementById('chart-policy-level'), null, { renderer: 'svg' });
  chart3.setOption({
    animation: false,
    tooltip: { trigger: 'item', appendToBody: true },
    series: [{
      type: 'pie',
      radius: '65%',
      center: ['50%', '50%'],
      itemStyle: { borderRadius: 4, borderColor: bg2, borderWidth: 2 },
      label: { show: true, color: ink, fontSize: 12, formatter: '{b}\n{d}%' },
      data: [
        { value: 3, name: '国家级', itemStyle: { color: accent } },
        { value: 2, name: '地方级', itemStyle: { color: accent2 } },
        { value: 4, name: '国外国家级', itemStyle: { color: muted } },
        { value: 2, name: '国外地方级', itemStyle: { color: accent + '99' } }
      ]
    }]
  });
  window.addEventListener('resize', function() { chart3.resize(); });

  // --- Chart: Tech Keyword Frequency ---
  var chart4 = echarts.init(document.getElementById('chart-tech-freq'), null, { renderer: 'svg' });
  chart4.setOption({
    animation: false,
    tooltip: { trigger: 'axis', appendToBody: true, axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '8%', bottom: '5%', top: '5%', containLabel: true },
    xAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: rule, type: 'dashed' } },
      axisLabel: { color: muted }
    },
    yAxis: {
      type: 'category',
      data: ['区块链', '物联网', 'REITs', '数据空间', 'CIM平台', '智能出行', '一网统管', '数字孪生', '数据要素', '人工智能'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: ink, fontSize: 12 },
      axisTick: { show: false }
    },
    series: [{
      type: 'bar',
      data: [2, 3, 3, 4, 5, 6, 7, 8, 9, 10],
      itemStyle: {
        color: function(params) {
          var colors = [accent, accent2, muted, accent + 'cc', accent2 + 'cc', muted + 'cc', accent + '99', accent2 + '99', muted + '99', accent];
          return colors[params.dataIndex] || accent;
        },
        borderRadius: [0, 4, 4, 0]
      },
      barWidth: '60%',
      label: { show: true, position: 'right', color: ink, fontSize: 11, formatter: '{c}次' }
    }]
  });
  window.addEventListener('resize', function() { chart4.resize(); });

  // --- Chart: Domestic Funding Scale ---
  var chart5 = echarts.init(document.getElementById('chart-funding'), null, { renderer: 'svg' });
  chart5.setOption({
    animation: false,
    tooltip: { trigger: 'axis', appendToBody: true, formatter: '{b}: {c}亿元' },
    grid: { left: '3%', right: '4%', bottom: '10%', top: '15%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['中央预算内投资', '超长期特别国债', '中央财政补助', '地方专项债', '社会资本'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 11, rotate: 15 }
    },
    yAxis: {
      type: 'value',
      name: '亿元',
      nameTextStyle: { color: muted },
      axisLine: { show: false },
      splitLine: { lineStyle: { color: rule, type: 'dashed' } },
      axisLabel: { color: muted }
    },
    series: [{
      type: 'bar',
      data: [970, 1600, 500, 800, 1200],
      itemStyle: {
        color: function(params) {
          var colors = [accent, accent2, muted, accent + 'cc', accent2 + 'cc'];
          return colors[params.dataIndex] || accent;
        },
        borderRadius: [4, 4, 0, 0]
      },
      barWidth: '50%',
      label: { show: true, position: 'top', color: ink, fontSize: 11, formatter: '{c}' }
    }]
  });
  window.addEventListener('resize', function() { chart5.resize(); });

  // --- Chart: International Investment Comparison ---
  var chart6 = echarts.init(document.getElementById('chart-invest'), null, { renderer: 'svg' });
  chart6.setOption({
    animation: false,
    tooltip: { trigger: 'axis', appendToBody: true },
    legend: { data: ['投资金额(亿美元)'], bottom: 0, textStyle: { color: muted } },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '10%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['新加坡AI投资', '韩国智慧城市', '欧盟数字欧洲', '欧盟LDT4SSC', '越南智慧城市'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted, fontSize: 10, rotate: 15 }
    },
    yAxis: {
      type: 'value',
      name: '亿美元',
      nameTextStyle: { color: muted },
      axisLine: { show: false },
      splitLine: { lineStyle: { color: rule, type: 'dashed' } },
      axisLabel: { color: muted }
    },
    series: [{
      name: '投资金额(亿美元)',
      type: 'bar',
      data: [7.5, 0.85, 0.63, 0.032, 0.5],
      itemStyle: { color: accent2, borderRadius: [4, 4, 0, 0] },
      barWidth: '50%',
      label: { show: true, position: 'top', color: ink, fontSize: 10, formatter: '{c}' }
    }]
  });
  window.addEventListener('resize', function() { chart6.resize(); });

  // --- Chart: Policy Trend Analysis ---
  var chart7 = echarts.init(document.getElementById('chart-trend'), null, { renderer: 'svg' });
  chart7.setOption({
    animation: false,
    tooltip: { trigger: 'axis', appendToBody: true },
    legend: { data: ['技术驱动', '数据驱动', '制度驱动', '运营驱动'], bottom: 0, textStyle: { color: muted } },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '10%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['2022年', '2023年', '2024年', '2025年', '2026年'],
      axisLine: { lineStyle: { color: rule } },
      axisLabel: { color: muted }
    },
    yAxis: {
      type: 'value',
      name: '政策关注度指数',
      nameTextStyle: { color: muted },
      axisLine: { show: false },
      splitLine: { lineStyle: { color: rule, type: 'dashed' } },
      axisLabel: { color: muted }
    },
    series: [
      {
        name: '技术驱动',
        type: 'line',
        data: [85, 80, 75, 70, 65],
        smooth: true,
        lineStyle: { color: muted, width: 2 },
        itemStyle: { color: muted },
        areaStyle: { color: muted + '20' }
      },
      {
        name: '数据驱动',
        type: 'line',
        data: [40, 55, 70, 82, 90],
        smooth: true,
        lineStyle: { color: accent, width: 3 },
        itemStyle: { color: accent },
        areaStyle: { color: accent + '20' }
      },
      {
        name: '制度驱动',
        type: 'line',
        data: [30, 35, 45, 60, 78],
        smooth: true,
        lineStyle: { color: accent2, width: 2 },
        itemStyle: { color: accent2 },
        areaStyle: { color: accent2 + '20' }
      },
      {
        name: '运营驱动',
        type: 'line',
        data: [25, 30, 40, 55, 72],
        smooth: true,
        lineStyle: { color: '#16a34a', width: 2 },
        itemStyle: { color: '#16a34a' },
        areaStyle: { color: '#16a34a20' }
      }
    ]
  });
  window.addEventListener('resize', function() { chart7.resize(); });

  window.resizeCharts = function() {
    chart1.resize();
    chart2.resize();
    chart3.resize();
    chart4.resize();
    chart5.resize();
    chart6.resize();
    chart7.resize();
  };
})();
