// Create DOM structure
document.head.innerHTML = '<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">';
document.title = 't-SNE 3D Visualization';

const style = document.createElement('style');
style.textContent = `
  body { margin: 0; font-family: sans-serif; background: #f4f4f4; }
  .container { display: flex; height: 100vh; }
  .vis-area { flex: 2; padding: 20px; background: white; }
  #vis-canvas { width: 100%; height: 100%; }
  .controls { flex: 1; max-width: 400px; padding: 20px; background: #f9f9f9; overflow-y: auto; }
  .control-group { margin: 15px 0; display: flex; align-items: center; }
  label { width: 120px; margin-right: 10px; }
  input { width: 80px; padding: 5px; }
  button { padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
`;
document.head.appendChild(style);

const container = document.createElement('div');
container.className = 'container';
document.body.appendChild(container);

const visArea = document.createElement('div');
visArea.className = 'vis-area';
container.appendChild(visArea);

const visTitle = document.createElement('h2');
visTitle.textContent = 't-SNE 3D Visualization';
visArea.appendChild(visTitle);

const visCanvas = document.createElement('div');
visCanvas.id = 'vis-canvas';
visArea.appendChild(visCanvas);

const statusDiv = document.createElement('div');
statusDiv.textContent = 'Status: Ready';
visArea.appendChild(statusDiv);

const controls = document.createElement('div');
controls.className = 'controls';
container.appendChild(controls);

const params = [
  {id: 'perplexity', label: 'Perplexity', value: 30, min: 5, max: 50},
  {id: 'learningRate', label: 'Learning Rate', value: 200, min: 10, max: 1000},
  {id: 'iterations', label: 'Iterations', value: 500, min: 100, max: 5000}
];

params.forEach(param => {
  const group = document.createElement('div');
  group.className = 'control-group';
  
  const label = document.createElement('label');
  label.textContent = param.label;
  group.appendChild(label);
  
  const input = document.createElement('input');
  Object.assign(input, {
    type: 'number',
    id: param.id,
    value: param.value,
    min: param.min,
    max: param.max
  });
  group.appendChild(input);
  
  controls.appendChild(group);
});

const runButton = document.createElement('button');
runButton.textContent = 'Run t-SNE';
controls.appendChild(runButton);

// Three.js Visualization
let scene, camera, renderer, controls3d, pointsGroup;
const colors = [0xff0000, 0x00ff00, 0x0000ff, 0xffff00, 0xff00ff];
let currentData = [];

function initThree() {
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(75, visCanvas.offsetWidth / visCanvas.offsetHeight, 0.1, 1000);
  renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(visCanvas.offsetWidth, visCanvas.offsetHeight);
  visCanvas.appendChild(renderer.domElement);
  
  controls3d = new THREE.OrbitControls(camera, renderer.domElement);
  camera.position.z = 50;
  
  pointsGroup = new THREE.Group();
  scene.add(pointsGroup);
  
  window.addEventListener('resize', () => {
    camera.aspect = visCanvas.offsetWidth / visCanvas.offsetHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(visCanvas.offsetWidth, visCanvas.offsetHeight);
  });
}

function generateData(points = 500, dimensions = 20, clusters = 5) {
  currentData = [];
  const labels = [];
  for(let i = 0; i < points; i++) {
    const cluster = i % clusters;
    currentData.push(Array.from({length: dimensions}, 
      () => (Math.random() + cluster) * 5));
    labels.push(cluster);
  }
  return {data: currentData, labels};
}

async function runTSNE() {
  const {data, labels} = generateData();
  const options = {
    dim: 3,
    perplexity: +document.getElementById('perplexity').value,
    learningRate: +document.getElementById('learningRate').value,
    nIter: +document.getElementById('iterations').value
  };

  const tsne = new TSNE(options);
  tsne.initSync(data);
  
  statusDiv.textContent = 'Optimizing...';
  runButton.disabled = true;
  
  for(let i = 0; i < options.nIter; i++) {
    tsne.step();
    if(i % 50 === 0) {
      updatePoints(tsne.getOutput(), labels);
      await new Promise(r => requestAnimationFrame(r));
    }
  }
  
  updatePoints(tsne.getOutput(), labels);
  runButton.disabled = false;
  statusDiv.textContent = 'Complete!';
}

function updatePoints(embedding, labels) {
  pointsGroup.clear();
  
  const geometry = new THREE.BufferGeometry();
  const positions = new Float32Array(embedding.flat());
  const colors = new Float32Array(labels.flatMap(l => {
    const color = new THREE.Color(this.colors[l % this.colors.length]);
    return [color.r, color.g, color.b];
  }));
  
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
  
  const material = new THREE.PointsMaterial({
    size: 0.3,
    vertexColors: true,
    transparent: true,
    opacity: 0.8
  });
  
  pointsGroup.add(new THREE.Points(geometry, material));
  renderer.render(scene, camera);
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  initThree();
  runButton.addEventListener('click', runTSNE);
});