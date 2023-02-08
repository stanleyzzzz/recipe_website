import { FormControl, InputLabel, MenuItem, Select } from '@mui/material'
import React, { useEffect } from 'react'

function SortByMenu({sort, setSort}) {

    return (
            <FormControl className="sortByMenu" sx={{ m: 1, minWidth: 120 }} size="small">
                <InputLabel id="demo-simple-select-label">Sort By</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        label="Sort By"
                        value={sort}
                        onChange={(e)=>{
                            setSort(e.target.value);
                            console.log(e.target.value)}}
                    >
                        <MenuItem value={"ratings"}>Highly Rated</MenuItem>
                        <MenuItem value={"reviews"}>Most Reviewed</MenuItem>
                    </Select>
            </FormControl>
    )
}

export default SortByMenu
