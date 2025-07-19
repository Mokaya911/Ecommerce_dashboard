{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "4f4857b6",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "\n",
       "        <iframe\n",
       "            width=\"100%\"\n",
       "            height=\"650\"\n",
       "            src=\"http://127.0.0.1:8050/\"\n",
       "            frameborder=\"0\"\n",
       "            allowfullscreen\n",
       "            \n",
       "        ></iframe>\n",
       "        "
      ],
      "text/plain": [
       "<IPython.lib.display.IFrame at 0x2a05042bed0>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import dash\n",
    "from dash import html, dcc\n",
    "import plotly.express as px\n",
    "\n",
    "# Load the data\n",
    "df = pd.read_csv(r\"C:\\Users\\user\\Desktop\\data analysis project\\datasets\\clean.csv\")\n",
    "\n",
    "# Convert OrderDate to datetime\n",
    "df[\"OrderDate\"] = pd.to_datetime(df[\"OrderDate\"], errors=\"coerce\")\n",
    "df = df.dropna(subset=['OrderDate'])\n",
    "\n",
    "# Add month and year columns\n",
    "df['Year'] = df['OrderDate'].dt.year\n",
    "df['Month'] = df['OrderDate'].dt.to_period('M').astype(str)\n",
    "\n",
    "# ----------- KPI Metrics -------------\n",
    "total_revenue = df['TotalPrice'].sum()\n",
    "total_orders = df['OrderID'].nunique()\n",
    "top_product = df.groupby('Product')['TotalPrice'].sum().idxmax()\n",
    "\n",
    "# ----------- Visualizations -------------\n",
    "\n",
    "# 1. Total Sales Over Time (Monthly)\n",
    "monthly_sales = df.groupby('Month')['TotalPrice'].sum().reset_index()\n",
    "fig1 = px.line(monthly_sales, x='Month', y='TotalPrice', title='📈 Total Sales Over Time (Monthly)')\n",
    "\n",
    "# 2. Top Products per Month\n",
    "top_products_month = df.groupby(['Month', 'Product'])['TotalPrice'].sum().reset_index()\n",
    "top_products_month = top_products_month.sort_values(['Month', 'TotalPrice'], ascending=[True, False])\n",
    "top_products_month = top_products_month.groupby('Month').head(5)\n",
    "fig2 = px.bar(top_products_month, x='Product', y='TotalPrice', color='Month', barmode='group',\n",
    "              title='🏆 Top 5 Products per Month')\n",
    "\n",
    "# 3. Top Categories per Year\n",
    "top_categories_year = df.groupby(['Year', 'Category'])['TotalPrice'].sum().reset_index()\n",
    "fig3 = px.bar(top_categories_year, x='Category', y='TotalPrice', color='Year', barmode='group',\n",
    "              title='📊 Top Categories per Year (by Revenue)')\n",
    "\n",
    "# 4. Products with Highest Revenue Overall\n",
    "top_products = df.groupby('Product')['TotalPrice'].sum().reset_index().sort_values(by='TotalPrice', ascending=False).head(10)\n",
    "fig4 = px.bar(top_products, x='Product', y='TotalPrice', title='💰 Top 10 Products by Revenue')\n",
    "\n",
    "# 5. Revenue Share by Category (Pie)\n",
    "fig5 = px.pie(df, names='Category', values='TotalPrice', title='🧩 Revenue Share by Category')\n",
    "\n",
    "# Initialize Dash App\n",
    "app = dash.Dash(__name__)\n",
    "app.title = 'Advanced Business Dashboard'\n",
    "\n",
    "# Dashboard Layout\n",
    "app.layout = html.Div([\n",
    "    html.H1(\"📊 Business Performance Dashboard\", style={'textAlign': 'center'}),\n",
    "\n",
    "    html.Div([\n",
    "        html.Div([\n",
    "            html.H4(\"✅ Total Revenue:\"),\n",
    "            html.P(f\"${total_revenue:,.2f}\"),\n",
    "        ], style={'width': '30%', 'display': 'inline-block'}),\n",
    "\n",
    "        html.Div([\n",
    "            html.H4(\"📦 Total Unique Orders:\"),\n",
    "            html.P(f\"{total_orders}\"),\n",
    "        ], style={'width': '30%', 'display': 'inline-block'}),\n",
    "\n",
    "        html.Div([\n",
    "            html.H4(\"🥇 Top Product by Revenue:\"),\n",
    "            html.P(f\"{top_product}\"),\n",
    "        ], style={'width': '30%', 'display': 'inline-block'}),\n",
    "    ], style={'textAlign': 'center', 'marginBottom': 40}),\n",
    "\n",
    "    dcc.Graph(figure=fig1),\n",
    "    dcc.Graph(figure=fig2),\n",
    "    dcc.Graph(figure=fig3),\n",
    "    dcc.Graph(figure=fig4),\n",
    "    dcc.Graph(figure=fig5),\n",
    "])\n",
    "\n",
    "# Run the server\n",
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)\n",
    "\n",
    "\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.13.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
