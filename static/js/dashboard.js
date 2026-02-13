/**
 * ShopifyPulse Dashboard JavaScript
 * Interactive charts and real-time updates
 */

// ========================================
// State Management
// ========================================

const state = {
    period: '30d',
    storeId: 'demo',
    isLoading: false
};

// ========================================
// Initialize Dashboard
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    loadRecommendations();
    setupEventListeners();
    animateCounters();
});

// ========================================
// Chart Initialization
// ========================================

function initializeCharts() {
    initRevenueChart();
    initTrafficChart();
    initFunnelChart();
    initDeviceChart();
}

function initRevenueChart() {
    const dates = [];
    const revenue = [];
    const orders = [];
    
    // Generate 30 days of sample data
    const baseRevenue = 6000;
    for (let i = 0; i < 30; i++) {
        const date = new Date();
        date.setDate(date.getDate() - (29 - i));
        dates.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        
        const dayOfWeek = date.getDay();
        const weekendBoost = (dayOfWeek === 0 || dayOfWeek === 6) ? 1.3 : 1;
        const randomFactor = 0.85 + Math.random() * 0.3;
        const growthFactor = 1 + (i * 0.002);
        
        const dayRevenue = Math.round(baseRevenue * weekendBoost * randomFactor * growthFactor);
        revenue.push(dayRevenue);
        orders.push(Math.round(dayRevenue / 78));
    }
    
    const trace1 = {
        x: dates,
        y: revenue,
        type: 'scatter',
        mode: 'lines',
        name: 'Revenue',
        line: {
            color: '#6366f1',
            width: 3,
            shape: 'spline'
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(99, 102, 241, 0.1)'
    };
    
    const trace2 = {
        x: dates,
        y: orders,
        type: 'bar',
        name: 'Orders',
        marker: {
            color: 'rgba(139, 92, 246, 0.5)'
        },
        yaxis: 'y2'
    };
    
    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#94a3b8', family: 'Inter, sans-serif' },
        margin: { t: 10, r: 50, b: 40, l: 60 },
        xaxis: {
            showgrid: false,
            tickangle: -45,
            nticks: 10
        },
        yaxis: {
            title: 'Revenue ($)',
            titlefont: { color: '#6366f1' },
            tickfont: { color: '#6366f1' },
            showgrid: true,
            gridcolor: 'rgba(255,255,255,0.05)',
            tickformat: '$,.0f'
        },
        yaxis2: {
            title: 'Orders',
            titlefont: { color: '#8b5cf6' },
            tickfont: { color: '#8b5cf6' },
            overlaying: 'y',
            side: 'right',
            showgrid: false
        },
        legend: {
            x: 0,
            y: 1.1,
            orientation: 'h',
            font: { color: '#f8fafc' }
        },
        hovermode: 'x unified'
    };
    
    const config = { responsive: true, displayModeBar: false };
    
    Plotly.newPlot('revenue-chart', [trace1, trace2], layout, config);
}

function initTrafficChart() {
    const data = [{
        values: [35, 25, 20, 15, 5],
        labels: ['Organic Search', 'Paid Ads', 'Social Media', 'Email', 'Direct'],
        type: 'pie',
        hole: 0.5,
        marker: {
            colors: ['#6366f1', '#8b5cf6', '#22c55e', '#f59e0b', '#3b82f6']
        },
        textinfo: 'label+percent',
        textposition: 'outside',
        automargin: true
    }];
    
    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#f8fafc', family: 'Inter, sans-serif' },
        margin: { t: 20, r: 20, b: 20, l: 20 },
        showlegend: false,
        annotations: [{
            text: 'Traffic<br>Sources',
            x: 0.5,
            y: 0.5,
            xref: 'paper',
            yref: 'paper',
            showarrow: false,
            font: { size: 14, color: '#f8fafc' }
        }]
    };
    
    Plotly.newPlot('traffic-chart', data, layout, { responsive: true, displayModeBar: false });
}

function initFunnelChart() {
    const stages = ['Visit', 'Product View', 'Add to Cart', 'Checkout', 'Purchase'];
    const values = [45000, 22500, 6750, 4050, 2458];
    const conversionRates = [100, 50, 30, 60, 60.7];
    
    const colors = ['#6366f1', '#8b5cf6', '#22c55e', '#f59e0b', '#ef4444'];
    
    const data = [{
        type: 'funnel',
        y: stages,
        x: values,
        textposition: 'inside',
        textinfo: 'value+percent initial',
        opacity: 0.85,
        marker: {
            color: colors,
            line: { color: '#1e293b', width: 2 }
        },
        connector: {
            line: { color: '#475569', width: 2, dash: 'dot' }
        }
    }];
    
    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#f8fafc', family: 'Inter, sans-serif' },
        margin: { t: 20, r: 100, b: 40, l: 120 },
        funnelmode: 'stack'
    };
    
    Plotly.newPlot('funnel-chart', data, layout, { responsive: true, displayModeBar: false });
}

function initDeviceChart() {
    const devices = ['Desktop', 'Mobile', 'Tablet'];
    const conversionRates = [6.2, 4.8, 5.5];
    const visitors = [18000, 22500, 4500];
    
    const data = [{
        x: devices,
        y: conversionRates,
        type: 'bar',
        marker: {
            color: ['#6366f1', '#8b5cf6', '#22c55e'],
            borderRadius: 8
        },
        text: conversionRates.map(r => r + '%'),
        textposition: 'outside',
        name: 'Conversion Rate'
    }];
    
    const layout = {
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        font: { color: '#f8fafc', family: 'Inter, sans-serif' },
        margin: { t: 30, r: 20, b: 40, l: 50 },
        xaxis: {
            showgrid: false
        },
        yaxis: {
            title: 'Conversion Rate (%)',
            showgrid: true,
            gridcolor: 'rgba(255,255,255,0.05)',
            range: [0, 8]
        },
        annotations: [
            {
                x: 'Mobile',
                y: 4.8,
                text: '⚠️ -22% vs Desktop',
                showarrow: true,
                arrowhead: 2,
                arrowcolor: '#f59e0b',
                font: { color: '#f59e0b', size: 10 },
                ax: 40,
                ay: -40
            }
        ]
    };
    
    Plotly.newPlot('device-chart', data, layout, { responsive: true, displayModeBar: false });
}

// ========================================
// Load Recommendations
// ========================================

function loadRecommendations() {
    // Simulated API response
    const recommendations = [
        {
            id: 'rec_001',
            title: 'Fix checkout abandonment spike',
            description: 'Your checkout abandonment increased 15% this week. 38% of users drop off at the shipping information step. Consider offering free shipping over $75 or showing shipping costs earlier.',
            category: 'conversion',
            priority: 'critical',
            impact_score: 92,
            effort_score: 25,
            potential_revenue: 8450,
            implementation_time: '2 hours',
            steps: [
                'Enable free shipping threshold banner on cart page',
                'Add shipping calculator to product pages',
                'Simplify checkout form fields'
            ],
            confidence: 0.89
        },
        {
            id: 'rec_002',
            title: 'Launch win-back email campaign',
            description: 'You have 3,240 customers who haven\'t purchased in 90+ days. These customers previously spent an average of $145. A targeted win-back campaign could recover 8-12% of them.',
            category: 'retention',
            priority: 'high',
            impact_score: 78,
            effort_score: 35,
            potential_revenue: 12400,
            implementation_time: '1 day',
            steps: [
                'Segment customers by last purchase date',
                'Create 3-email win-back sequence',
                'Offer 15% discount in final email',
                'Set up automated trigger'
            ],
            confidence: 0.85
        },
        {
            id: 'rec_003',
            title: 'Optimize mobile product pages',
            description: 'Mobile visitors convert 22% lower than desktop. Analysis shows slow image loading and confusing CTA placement. Mobile represents 50% of your traffic but only 38% of revenue.',
            category: 'conversion',
            priority: 'high',
            impact_score: 85,
            effort_score: 45,
            potential_revenue: 18600,
            implementation_time: '3 days',
            steps: [
                'Compress product images (currently 2.3MB avg)',
                'Move CTA above the fold',
                'Implement lazy loading',
                'Add sticky Add to Cart button'
            ],
            confidence: 0.91
        },
        {
            id: 'rec_004',
            title: 'Increase AOV with bundle offers',
            description: 'Customers who buy "Vintage Denim Jacket" often also buy "Graphic Tees" within 14 days. Creating a bundle could increase AOV by $32 and conversion by 18%.',
            category: 'revenue',
            priority: 'medium',
            impact_score: 72,
            effort_score: 20,
            potential_revenue: 9600,
            implementation_time: '4 hours',
            steps: [
                'Create "Street Style Bundle" with jacket + 2 tees',
                'Price at $129 (saving of $25)',
                'Promote on homepage and PDP',
                'A/B test bundle vs. individual products'
            ],
            confidence: 0.82
        }
    ];
    
    renderRecommendations(recommendations);
}

function renderRecommendations(recommendations) {
    const container = document.getElementById('recommendations-list');
    
    container.innerHTML = recommendations.map(rec => `
        <div class="recommendation-card" data-id="${rec.id}">
            <div class="rec-header">
                <div class="rec-title-row">
                    <h3 class="rec-title">${rec.title}</h3>
                    <div class="rec-badges">
                        <span class="badge badge-${rec.priority}">${rec.priority}</span>
                        <span class="badge badge-${rec.category}">${rec.category}</span>
                    </div>
                </div>
            </div>
            <p class="rec-description">${rec.description}</p>
            <div class="rec-metrics">
                <div class="rec-metric">
                    <span class="rec-metric-label">Potential Revenue</span>
                    <span class="rec-metric-value revenue">+$${rec.potential_revenue.toLocaleString()}/mo</span>
                </div>
                <div class="rec-metric">
                    <span class="rec-metric-label">Impact Score</span>
                    <span class="rec-metric-value">${rec.impact_score}/100</span>
                </div>
                <div class="rec-metric">
                    <span class="rec-metric-label">Effort Required</span>
                    <span class="rec-metric-value">${rec.effort_score < 30 ? 'Low' : rec.effort_score < 50 ? 'Medium' : 'High'}</span>
                </div>
                <div class="rec-metric">
                    <span class="rec-metric-label">Time to Implement</span>
                    <span class="rec-metric-value">${rec.implementation_time}</span>
                </div>
            </div>
            <div class="rec-actions">
                <button class="btn btn-primary" onclick="implementRecommendation('${rec.id}')">
                    Start Implementation
                </button>
                <button class="btn btn-outline" onclick="dismissRecommendation('${rec.id}')">
                    Dismiss
                </button>
                <span class="rec-steps-toggle" onclick="toggleSteps('${rec.id}')">
                    View Implementation Steps
                </span>
            </div>
            <div class="rec-steps" id="steps-${rec.id}">
                <ol>
                    ${rec.steps.map(step => `<li>${step}</li>`).join('')}
                </ol>
            </div>
        </div>
    `).join('');
}

// ========================================
// Event Listeners
// ========================================

function setupEventListeners() {
    // Period selector
    document.querySelectorAll('.period-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            state.period = e.target.dataset.period;
            refreshDashboard();
        });
    });
    
    // Recommendation filters
    document.querySelectorAll('.rec-filter').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.rec-filter').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            filterRecommendations(e.target.textContent);
        });
    });
    
    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// ========================================
// Actions
// ========================================

function implementRecommendation(id) {
    showNotification('Implementation started! Check your email for detailed steps.', 'success');
    
    // Track in analytics
    console.log('Recommendation implemented:', id);
}

function dismissRecommendation(id) {
    const card = document.querySelector(`[data-id="${id}"]`);
    if (card) {
        card.style.opacity = '0';
        card.style.transform = 'translateX(-20px)';
        setTimeout(() => card.remove(), 300);
    }
    
    showNotification('Recommendation dismissed', 'info');
}

function toggleSteps(id) {
    const steps = document.getElementById(`steps-${id}`);
    steps.classList.toggle('expanded');
}

function filterRecommendations(filter) {
    const cards = document.querySelectorAll('.recommendation-card');
    
    cards.forEach(card => {
        const priority = card.querySelector('.badge-critical, .badge-high, .badge-medium').textContent.toLowerCase();
        
        if (filter === 'All' || 
            (filter === 'Critical' && priority === 'critical') ||
            (filter === 'High Impact' && priority === 'high') ||
            (filter === 'Quick Wins' && card.textContent.includes('Low'))) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function refreshDashboard() {
    showNotification(`Dashboard refreshed for ${state.period} period`, 'info');
    
    // Re-initialize charts with new data
    initializeCharts();
}

// ========================================
// Utilities
// ========================================

function animateCounters() {
    const counters = document.querySelectorAll('.kpi-value');
    
    counters.forEach(counter => {
        const target = parseFloat(counter.textContent.replace(/[^0-9.]/g, ''));
        const prefix = counter.textContent.includes('$') ? '$' : '';
        const suffix = counter.textContent.includes('%') ? '%' : '';
        const isDecimal = target % 1 !== 0;
        
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            
            let formatted = isDecimal ? current.toFixed(2) : Math.round(current).toLocaleString();
            counter.textContent = prefix + formatted + suffix;
        }, 20);
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Handle window resize for charts
window.addEventListener('resize', () => {
    Plotly.Plots.resize('revenue-chart');
    Plotly.Plots.resize('traffic-chart');
    Plotly.Plots.resize('funnel-chart');
    Plotly.Plots.resize('device-chart');
});
