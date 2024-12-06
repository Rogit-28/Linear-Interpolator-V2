#![cfg_attr(all(not(debug_assertions), target_os = "windows"), windows_subsystem = "windows")]

use tauri::{Manager, WindowBuilder, WindowUrl};

fn main() {
    tauri::Builder::default()
        .setup(|app| {
            // Start the Python backend server
            std::thread::spawn(|| {
                let backend = std::process::Command::new("python")
                    .args(&["-m", "backend.tauri_backend"])
                    .current_dir("backend")
                    .spawn()
                    .expect("Failed to start backend server");
                
                // Wait for the backend process
                let _ = backend.wait();
            });

            // Create the main window
            let window = WindowBuilder::new(app, "main", WindowUrl::default())
                .title("Scaling Range")
                .resizable(false)
                .build()
                .expect("Failed to create window");

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("Error while running tauri application");
}
