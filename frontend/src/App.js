import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import './App.css';

const Dashboard = () => {
  const [metrics] = useState({
    recommendationsServed: '2.4M',
    clickThroughRate: '8.4%',
    userEngagement: '74%',
    responseTime: '12ms'
  });

  const [engagementData] = useState([
    { day: 'Mon', ctr: 6.2, saves: 12.1 },
    { day: 'Tue', ctr: 7.1, saves: 13.5 },
    { day: 'Wed', ctr: 8.4, saves: 15.2 },
    { day: 'Thu', ctr: 7.8, saves: 14.8 },
    { day: 'Fri', ctr: 9.2, saves: 16.3 },
    { day: 'Sat', ctr: 8.7, saves: 15.9 },
    { day: 'Sun', ctr: 8.4, saves: 15.1 }
  ]);

  const [categoryData] = useState([
    { name: 'Food', value: 28, color: '#e60023' },
    { name: 'Fashion', value: 22, color: '#ff4081' },
    { name: 'Home Decor', value: 18, color: '#9c27b0' },
    { name: 'DIY', value: 15, color: '#673ab7' },
    { name: 'Travel', value: 12, color: '#3f51b5' },
    { name: 'Others', value: 5, color: '#2196f3' }
  ]);

  const [trendingPins] = useState([
    { title: 'Modern Kitchen Ideas', category: 'Home Decor', saves: '3.2k', score: 95.8 },
    { title: 'Spring Fashion Trends', category: 'Fashion', saves: '2.8k', score: 91.2 },
    { title: 'DIY Organization Hacks', category: 'DIY', saves: '2.1k', score: 87.5 },
    { title: 'Healthy Breakfast Ideas', category: 'Food', saves: '1.9k', score: 84.3 }
  ]);

  const [recommendations] = useState([
    {
      title: 'Living Room Decor Ideas',
      reason: 'Recommended for user jane_doe based on Home Decor preference',
      score: 89.5,
      category: 'HOME'
    },
    {
      title: 'Quick Dinner Recipes',
      reason: 'Popular with similar users who like cooking',
      score: 76.2,
      category: 'FOOD'
    },
    {
      title: 'Digital Art Tutorials',
      reason: 'Trending in Art category',
      score: 82.7,
      category: 'ART'
    }
  ]);

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb' }}>
      {/* Header */}
      <div style={{ 
        background: 'linear-gradient(to right, #ef4444, #dc2626)', 
        color: 'white', 
        padding: '2rem 1.5rem' 
      }}>
        <div style={{ maxWidth: '80rem', margin: '0 auto' }}>
          <h1 style={{ fontSize: '2.25rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
            Pinterest Recommender Dashboard
          </h1>
          <p style={{ opacity: 0.9 }}>Real-time analytics and recommendation performance</p>
        </div>
      </div>

      <div style={{ maxWidth: '80rem', margin: '0 auto', padding: '2rem 1.5rem' }}>
        {/* Key Metrics */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
          gap: '1.5rem', 
          marginBottom: '2rem' 
        }}>
          <MetricCard 
            label="Recommendations Served" 
            value={metrics.recommendationsServed} 
            change="+15.2% this week" 
          />
          <MetricCard 
            label="Click-Through Rate" 
            value={metrics.clickThroughRate} 
            change="+2.1% this week" 
          />
          <MetricCard 
            label="User Engagement" 
            value={metrics.userEngagement} 
            change="+5.8% this week" 
          />
          <MetricCard 
            label="Response Time" 
            value={metrics.responseTime} 
            change="-38% faster" 
          />
        </div>

        {/* Charts Section */}
        <div style={{ 
          backgroundColor: 'white', 
          borderRadius: '0.5rem', 
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)', 
          marginBottom: '2rem' 
        }}>
          <div style={{ borderBottom: '1px solid #e5e7eb', padding: '1.5rem' }}>
            <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827' }}>
              Engagement Trends
            </h3>
          </div>
          <div style={{ padding: '1.5rem' }}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '2rem' }}>
              {/* Line Chart */}
              <div>
                <h4 style={{ fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '1rem' }}>
                  Weekly Engagement
                </h4>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={engagementData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="day" />
                    <YAxis />
                    <Tooltip />
                    <Line 
                      type="monotone" 
                      dataKey="ctr" 
                      stroke="#e60023" 
                      strokeWidth={3}
                      name="Click-Through Rate (%)"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {/* Pie Chart */}
              <div>
                <h4 style={{ fontSize: '0.875rem', fontWeight: '500', color: '#374151', marginBottom: '1rem' }}>
                  Popular Categories
                </h4>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {categoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </div>

        {/* Trending Pins and Recommendations */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '2rem' }}>
          {/* Trending Pins */}
          <div style={{ 
            backgroundColor: 'white', 
            borderRadius: '0.5rem', 
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)' 
          }}>
            <div style={{ borderBottom: '1px solid #e5e7eb', padding: '1.5rem' }}>
              <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827' }}>
                Trending Pins Right Now
              </h3>
            </div>
            <div style={{ padding: '1.5rem' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem' }}>
                {trendingPins.map((pin, index) => (
                  <TrendingPinCard key={index} pin={pin} />
                ))}
              </div>
            </div>
          </div>

          {/* Recent Recommendations */}
          <div style={{ 
            backgroundColor: 'white', 
            borderRadius: '0.5rem', 
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)' 
          }}>
            <div style={{ borderBottom: '1px solid #e5e7eb', padding: '1.5rem' }}>
              <h3 style={{ fontSize: '1.125rem', fontWeight: '600', color: '#111827' }}>
                Recent Recommendations
              </h3>
            </div>
            <div style={{ padding: '1.5rem' }}>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {recommendations.map((rec, index) => (
                  <RecommendationCard key={index} recommendation={rec} />
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div style={{ marginTop: '3rem', textAlign: 'center', color: '#6b7280', fontSize: '0.875rem' }}>
          <p>Pinterest Trending Pins Recommender - Built with Django, React, and Machine Learning</p>
          <p style={{ marginTop: '0.25rem' }}>
            Scalable recommendation engine with 50% improved content delivery latency
          </p>
        </div>
      </div>
    </div>
  );
};

const MetricCard = ({ label, value, change }) => (
  <div style={{ 
    backgroundColor: 'white', 
    borderRadius: '0.5rem', 
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)', 
    padding: '1.5rem', 
    textAlign: 'center' 
  }}>
    <div style={{ fontSize: '0.875rem', color: '#6b7280', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
      {label}
    </div>
    <div style={{ fontSize: '1.875rem', fontWeight: 'bold', color: '#e60023', marginBottom: '0.5rem' }}>
      {value}
    </div>
    <div style={{ fontSize: '0.875rem', color: '#10b981' }}>
      {change}
    </div>
  </div>
);

const TrendingPinCard = ({ pin }) => (
  <div style={{ backgroundColor: '#f9fafb', borderRadius: '0.5rem', padding: '1rem', textAlign: 'center' }}>
    <div style={{ 
      width: '100%', 
      height: '6rem', 
      background: 'linear-gradient(to right, #fbbf24, #f59e0b)', 
      borderRadius: '0.5rem', 
      marginBottom: '0.75rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontWeight: 'bold',
      fontSize: '0.875rem'
    }}>
      {pin.category.toUpperCase()}
    </div>
    <div style={{ fontSize: '0.875rem', fontWeight: '600', marginBottom: '0.5rem' }}>
      {pin.title}
    </div>
    <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
      {pin.saves} saves • {pin.score} trending score
    </div>
  </div>
);

const RecommendationCard = ({ recommendation }) => (
  <div style={{ 
    display: 'flex', 
    alignItems: 'center', 
    padding: '1rem', 
    backgroundColor: '#f9fafb', 
    borderRadius: '0.5rem' 
  }}>
    <div style={{ 
      width: '3rem', 
      height: '3rem', 
      background: 'linear-gradient(to right, #ec4899, #e11d48)', 
      borderRadius: '0.5rem',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontWeight: 'bold',
      fontSize: '0.75rem',
      marginRight: '1rem'
    }}>
      {recommendation.category}
    </div>
    <div style={{ flex: 1 }}>
      <div style={{ fontWeight: '600', fontSize: '0.875rem', marginBottom: '0.25rem' }}>
        {recommendation.title}
      </div>
      <div style={{ fontSize: '0.75rem', color: '#6b7280' }}>
        {recommendation.reason}
      </div>
    </div>
    <div style={{ fontWeight: 'bold', color: '#e60023', fontSize: '1.125rem' }}>
      {recommendation.score}
    </div>
  </div>
);

export default Dashboard;