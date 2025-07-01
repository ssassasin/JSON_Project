import json

infile= open('univ.json', 'r')
outfile= open('readable_univ_data.json', 'w')

univ_data= json.load(infile)
json.dump(univ_data, outfile, indent=4)

big12= []

for school in univ_data:
    if "NCAA" in school:
        if school["NCAA"].get("NAIA conference number football (IC2020)") == 108:
            big12.append(school)

print(f"Number of Big 12 Schools: {len(big12)}")

enrollments, lons, lats, hover_texts= [], [], [], []

for school in big12:
    name= school["instnm"]
    w_address= school.get("Institution's internet website address (HD2020)", "")
    total= school["Total  enrollment (DRVEF2020)"]
    percent_women= school["Percent of total enrollment that are women (DRVEF2020)"]
    female= round(total*percent_women/100)
    male= total- female
    lat= school["Latitude location of institution (HD2020)"]
    lon= school["Longitude location of institution (HD2020)"]
    

    hover= f"{name}\n{w_address}\nTotal: {total:,}\nMale: {male:,}\nFemale: {female:,}"
    
    enrollments.append(total)
    lats.append(lat)
    lons.append(lon)
    hover_texts.append(hover)

    print(enrollments[:3])
    print(lats[:3])
    print(lons[:3])

    from plotly.graph_objs import Scattergeo, Layout
    from plotly import offline

    data= [{
        'type': 'scattergeo',
        'lon': lons,
        'lat': lats,
        'text': hover_texts,
        'marker': {
            'size': [e/1000 for e in enrollments],
            'color': enrollments,
            'colorscale': 'Viridis',
            'reversescale': False,
            'colorbar': {'title': 'Total Enrollment'}
        }

    }]

my_layout= Layout(title= 'Big 12 Universities Enrollment')
fig= {'data': data, 'layout': my_layout}
offline.plot(fig, filename= 'big12_universities_map.html')

    