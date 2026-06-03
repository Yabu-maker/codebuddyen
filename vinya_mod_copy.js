// vinya_mod.js - 30行Node.js实用模块
const fs = require('fs').promises;
const path = require('path');

// 生成随机数据
function generateRandomData(count = 5) {
  return Array.from({length: count}, (_, i) => ({
    id: i + 1,
    key: `item_${Math.random().toString(36).substring(2, 8)}`,
    value: Math.floor(Math.random() * 1000)
  }));
}

// 保存JSON文件
async function saveToJson(filename, data) {
  try {
    const filePath = path.join(__dirname, filename);
    await fs.writeFile(filePath, JSON.stringify(data, null, 2));
    console.log(`数据已保存至 ${filename}`);
    return true;
  } catch (err) {
    console.error('文件保存失败:', err);
    return false;
  }
}

// 主函数
async function main() {
  console.log('=== VINYA数据模块运行中 ===');
  
  // 生成并保存数据
  const data = generateRandomData();
  await saveToJson('vinya_data.json', data);
  
  // 数据分析
  const total = data.reduce((sum, item) => sum + item.value, 0);
  console.log(`生成${data.length}条记录，总值: ${total}`);
  
  // 文件信息
  const files = await fs.readdir(__dirname);
  console.log(`当前目录文件数: ${files.length}`);
  
  console.log('=== 模块执行完成 ===');
}

main();