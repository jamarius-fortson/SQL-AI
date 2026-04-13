import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional, Any

class ResultVisualizer:
    """Enterprise-grade automatic data visualization"""
    
    # Sophisticated, high-contrast color palette
    COLORS = ['#00e5ff', '#0062ff', '#7000ff', '#ff007a', '#00ffab']
    
    @staticmethod
    def should_visualize(df: pd.DataFrame) -> bool:
        if df.empty or len(df) < 1:
            return False
        return len(df.select_dtypes(include=['number']).columns) > 0
    
    @staticmethod
    def auto_visualize(df: pd.DataFrame, title: str = "Analysis Results") -> Optional[Any]:
        if not ResultVisualizer.should_visualize(df):
            return None
        
        # Internal copy to preserve original dataframe
        plot_df = df.copy()
        
        # Clean columns for display
        plot_df.columns = [c.replace('_', ' ').title() for c in plot_df.columns]
        
        numeric_cols = plot_df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = plot_df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # Detect date-like columns
        date_cols = []
        for col in categorical_cols:
            if any(key in col.lower() for key in ['date', 'time', 'month', 'year']):
                try:
                    plot_df[col] = pd.to_datetime(plot_df[col])
                    date_cols.append(col)
                except:
                    pass
        
        categorical_cols = [c for c in categorical_cols if c not in date_cols]

        try:
            # Logic: Choose the most descriptive chart type
            if date_cols and numeric_cols:
                # Line chart for time-series
                fig = px.line(plot_df, x=date_cols[0], y=numeric_cols[0], title=title,
                             template="plotly_dark", color_discrete_sequence=ResultVisualizer.COLORS)
                fig.update_traces(line=dict(width=4, shape='spline'))
            
            elif categorical_cols and numeric_cols:
                # Bar or Pie for categories
                if len(plot_df) <= 6 and len(numeric_cols) == 1:
                    fig = px.pie(plot_df, names=categorical_cols[0], values=numeric_cols[0], title=title,
                                hole=0.5, template="plotly_dark", color_discrete_sequence=ResultVisualizer.COLORS)
                else:
                    fig = px.bar(plot_df, x=categorical_cols[0], y=numeric_cols[0], title=title,
                                template="plotly_dark", color_discrete_sequence=ResultVisualizer.COLORS)
                    fig.update_traces(marker_line_color='rgba(255,255,255,0.1)', marker_line_width=1)
            
            elif len(numeric_cols) >= 2:
                fig = px.scatter(plot_df, x=numeric_cols[0], y=numeric_cols[1], title=title,
                                template="plotly_dark", color_discrete_sequence=ResultVisualizer.COLORS,
                                size=numeric_cols[1] if len(numeric_cols) > 1 else None)
            else:
                fig = px.bar(plot_df, y=numeric_cols[0], title=title,
                            template="plotly_dark", color_discrete_sequence=ResultVisualizer.COLORS)

            # Modern Aesthetic Upgrades
            fig.update_layout(
                font_family="Outfit",
                title_font_size=22,
                title_x=0.01,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#94a3b8")),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, tickfont=dict(color="#94a3b8")),
                margin=dict(l=50, r=20, t=80, b=50),
                legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color="#e2e8f0")),
                hoverlabel=dict(bgcolor="#0d1117", font_size=14, font_family="Outfit")
            )
            return fig
        except Exception as e:
            print(f"Visualization pipeline exception: {e}")
            return None

    @staticmethod
    def get_summary_stats(df: pd.DataFrame) -> str:
        numeric_df = df.select_dtypes(include=['number'])
        if numeric_df.empty:
            return f"Volumetric Analysis: {len(df)} records isolated."
            
        summary = f"Statistical Snapshot ({len(df)} records):\n"
        for col in numeric_df.columns:
            clean_name = col.replace('_', ' ').title()
            val_sum = numeric_df[col].sum()
            val_avg = numeric_df[col].mean()
            
            if any(key in col.lower() for key in ['price', 'amount', 'total', 'revenue', 'cost']):
                summary += f"• {clean_name}: Aggregated sum is ${val_sum:,.2f} | Mean: ${val_avg:,.2f}\n"
            else:
                summary += f"• {clean_name}: Combined sum {val_sum:,.0f} | Average {val_avg:,.1f}\n"
        return summary
