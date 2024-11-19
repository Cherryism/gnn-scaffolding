window.addEventListener('load', async function() {
    let data = await fetch("/input-data");
    let cytoData = await data.json();
    var cy = cytoscape({

        container: document.getElementById('cyto'), // container to render in
    
        elements: cytoData,
    
        style: [ // the stylesheet for the graph
            {
                selector: 'node',
                style: {
                    'background-color': '#666',
                    'label': 'data(id)',
                    'shape': 'tag'
                }
            },
    
            {
                selector: 'edge',
                style: {
                    'width': 3,
                    'line-color': '#ccc',
                    'target-arrow-color': '#ccc',
                    'target-arrow-shape': 'triangle',
                    'curve-style': 'bezier'
                }
            }
        ],
    
        layout: {
            name: 'grid',
            rows: 1
        }
    
    });
    
    cy.on('mouseover', 'edge', function (ev) {
        let targetEdge = ev.target;
        targetEdge.style('label', targetEdge.data().feature)
    })
    
    cy.on('mouseout', 'edge', function (ev) {
        let targetEdge = ev.target;
        targetEdge.style('label', null)
    })
})