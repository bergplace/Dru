# Using email notifications
- type and send your email address in box above
- click verification link you'll get in email
- now you can POST your email to the result links in form of ```{"email": "joe.doe@mail.com"}``` so that you'll 
be notified when the task has finished 


# Available APIs


- Current height of collected blockchain
    - ```/api/current_block_height```
    
- Blocks
    - ```/api/get_blocks/<start_height>/<end_height>```

- Blocks with reduced amount of info
    - ```/api/get_blocks_reduced/<start_height>/<end_height>```

- Edges of transaction graph
    - ```/api/get_edges/<start_height>/<end_height>```

- Degree of transaction graph
    - ```/api/get_degree/<start_height>/<end_height>/<mode: all|in|out>```

- Degree of transaction graph by block
    - ```/api/get_degree_by_block/<start_height>/end_height>/<address>/<mode: all|in|out>```

- Max degree
    - ```/api/get_degree_max/<start_height>/<end_height>/<all|in|out>```

- Betweenness
    - ```/api/get_betweenness/<start_height>/<end_height>/<directed: true|false>```

- Max betweenness
    - ```/api/get_betweenness_max/<start_height>/<end_height>/<directed: true|false>```

- Closeness
    - ```/api/get_closeness/<start_height>/<end_height>/<directed: true|false>```

- Max closeness
    - ```/api/get_closeness_max/<start_height>/<end_height>/<directed: true|false>```

- Transitivity
    - ```/api/get_transitivity/<start_height>/<end_height>```

- Global transitivity
    - ```/api/get_transitivity_global/<start_height>/<end_height>```

- Diameter
    - ```/api/get_diameter/<start_height>/<end_height>/<directed: true|false>```

- Density
    - ```/api/get_density/<start_height>/<end_height>/<directed: true|false>/<loops: true|false>```

- Are connected
    - ```/api/get_density/<start_height>/<end_height>/<address-1>/<address-2>/<directed: true|false>```

- Transactions value
    - ```/api/get_density/<start_height>/<end_height>/<address-1>/<address-2>/<directed: true|false>```
