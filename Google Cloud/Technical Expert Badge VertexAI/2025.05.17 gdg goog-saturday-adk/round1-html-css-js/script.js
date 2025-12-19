document.addEventListener('DOMContentLoaded', () => {
    const numPointsInput = document.getElementById('numPoints');
    const runTSNEButton = document.getElementById('runTSNE');
    const threeContainer = document.getElementById('three-container');
    const tsneCanvas = document.getElementById('tsne-canvas');
    const ctx = tsneCanvas.getContext('2d');

    let scene, camera, renderer, controls;
    let points3D = [];
    let pointColors = [];
    let threeJSPoints = new THREE.Group(); // Group to hold 3D points

    // Initialize Three.js scene
    function initThreeJS() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff); // White background

        camera = new THREE.PerspectiveCamera(75, threeContainer.clientWidth / threeContainer.clientHeight, 0.1, 1000);
        camera.position.z = 5;

        renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(threeContainer.clientWidth, threeContainer.clientHeight);
        threeContainer.appendChild(renderer.domElement);

        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true; // Animate controls
        controls.dampingFactor = 0.25;
        controls.screenSpacePanning = false;
        controls.maxPolarAngle = Math.PI / 2;

        // Add axes helper
        const axesHelper = new THREE.AxesHelper(5); // Size of axes
        scene.add(axesHelper);

        scene.add(threeJSPoints); // Add the group to the scene

        animate(); // Start animation loop
    }

    // Animation loop for Three.js
    function animate() {
        requestAnimationFrame(animate);
        controls.update(); // Only required if controls.enableDamping = true, or if controls.autoRotate = true
        renderer.render(scene, camera);
    }

    // Generate synthetic 3D data with clusters
    function generateData(numPoints) {
        points3D = [];
        pointColors = [];
        const numClusters = 4;
        const clusterCenters = [
            new THREE.Vector3(2, 2, 2),
            new THREE.Vector3(-2, -2, 2),
            new THREE.Vector3(2, -2, -2),
            new THREE.Vector3(-2, 2, -2)
        ];
        const clusterColors = [
            new THREE.Color(0xff0000), // Red
            new THREE.Color(0x00ff00), // Green
            new THREE.Color(0x0000ff), // Blue
            new THREE.Color(0xffff00)  // Yellow
        ];
        const noise = 0.5;

        for (let i = 0; i < numPoints; i++) {
            const clusterIndex = Math.floor(Math.random() * numClusters);
            const center = clusterCenters[clusterIndex];
            const color = clusterColors[clusterIndex];

            const point = new THREE.Vector3(
                center.x + (Math.random() - 0.5) * noise,
                center.y + (Math.random() - 0.5) * noise,
                center.z + (Math.random() - 0.5) * noise
            );

            points3D.push([point.x, point.y, point.z]); // Store as array for tsne-js
            pointColors.push(color);
        }
    }

    // Clear previous visualizations
    function clearVisualizations() {
        // Clear Three.js points
        while (threeJSPoints.children.length > 0) {
            threeJSPoints.remove(threeJSPoints.children[0]);
        }

        // Clear 2D canvas
        ctx.clearRect(0, 0, tsneCanvas.width, tsneCanvas.height);
    }

    // Render 3D points
    function render3DPoints() {
        const geometry = new THREE.BufferGeometry();
        const positions = [];
        const colors = [];
        const sizes = [];

        for (let i = 0; i < points3D.length; i++) {
            const point = points3D[i];
            const color = pointColors[i];

            positions.push(point[0], point[1], point[2]);
            colors.push(color.r, color.g, color.b);
            sizes.push(0.1); // Point size
        }

        geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
        geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
        geometry.setAttribute('size', new THREE.Float32BufferAttribute(sizes, 1));

        const material = new THREE.PointsMaterial({
            size: 0.2, // Base size, 'size' attribute is multiplied by this
            vertexColors: true,
            transparent: true,
            alphaTest: 0.5
        });

        const points = new THREE.Points(geometry, material);
        threeJSPoints.add(points);
    }

    // Run t-SNE and render 2D points
    function runTSNE() {
        clearVisualizations();
        const numPoints = parseInt(numPointsInput.value, 10);
        if (isNaN(numPoints) || numPoints < 10) {
            alert("Please enter a valid number of points (at least 10).");
            return;
        }

        generateData(numPoints);
        render3DPoints();

        // Configure and run t-SNE
        const opt = {};
        opt.epsilon = 10; // learning rate
        opt.perplexity = 30; // number of neighbors
        opt.dim = 2; // output dimensionality

        const tsne = new tsnejs.tSNE(opt);
        tsne.initDataRaw(points3D);

        // Run t-SNE for a fixed number of iterations
        const numIterations = 300;
        for (let i = 0; i < numIterations; i++) {
            tsne.step();
        }

        const Y = tsne.getSolution(); // Get 2D embedding

        // Draw 2D points on canvas
        const canvasWidth = tsneCanvas.width;
        const canvasHeight = tsneCanvas.height;
        const padding = 20;

        // Find min/max for scaling
        let minY = Infinity, maxY = -Infinity, minX = Infinity, maxX = -Infinity;
        for (let i = 0; i < Y.length; i++) {
            minX = Math.min(minX, Y[i][0]);
            maxX = Math.max(maxX, Y[i][0]);
            minY = Math.min(minY, Y[i][1]);
            maxY = Math.max(maxY, Y[i][1]);
        }

        const scaleX = (canvasWidth - 2 * padding) / (maxX - minX);
        const scaleY = (canvasHeight - 2 * padding) / (maxY - minY);
        const scale = Math.min(scaleX, scaleY); // Use uniform scale

        ctx.clearRect(0, 0, canvasWidth, canvasHeight); // Clear canvas before drawing

        for (let i = 0; i < Y.length; i++) {
            const x = (Y[i][0] - minX) * scale + padding;
            const y = (Y[i][1] - minY) * scale + padding; // Invert y for canvas coordinates

            ctx.beginPath();
            ctx.arc(x, y, 3, 0, 2 * Math.PI, false); // Draw a circle for each point
            ctx.fillStyle = '#' + pointColors[i].getHexString(); // Use the same color as 3D point
            ctx.fill();
        }
    }

    // Initialize Three.js on page load
    initThreeJS();

    // Add event listener to the button
    runTSNEButton.addEventListener('click', runTSNE);

    // Initial run with default points
    runTSNE();

    // Handle window resize
    window.addEventListener('resize', () => {
        // Update Three.js renderer size and camera aspect ratio
        renderer.setSize(threeContainer.clientWidth, threeContainer.clientHeight);
        camera.aspect = threeContainer.clientWidth / threeContainer.clientHeight;
        camera.updateProjectionMatrix();

        // Update canvas size and redraw 2D points
        tsneCanvas.width = threeContainer.clientWidth; // Match 3D container width
        tsneCanvas.height = 400; // Keep height consistent
        if (points3D.length > 0) {
             // Re-run t-SNE and redraw 2D points with new canvas size
             // Note: Re-running t-SNE every resize might be slow for many points.
             // A better approach for responsiveness would be to store the 2D points
             // and just redraw them with the new scaling. For simplicity, we re-run here.
             runTSNE();
        }
    });
});