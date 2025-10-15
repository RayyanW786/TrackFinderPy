use pyo3::prelude::*;

#[pyfunction]
fn version() -> PyResult<String> {
    Ok("trackfinder-py 0.1.0".to_string())
}

#[pymodule]
fn trackfinder_py(_py: Python, m: &Bound<PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(version, m)?)?;
    Ok(())
}
