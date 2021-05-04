use core::marker;

pub struct PlterJsValue {
    pub idx: u32,
    _marker: marker::PhantomData<*mut u8>,
}