package com.example;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public final class PythonRunner {

    public static void main(String[] args) throws IOException, InterruptedException {
        if (args.length > 1) {
            System.err.println("Usage: java -jar veg-stock-1.0.0.jar [path-to-workbook]");
            System.exit(2);
            return;
        }

        Path workbook = Path.of(args.length == 0 ? "Veg.xlsx" : args[0])
                .toAbsolutePath().normalize();
        if (args.length == 0 && Files.notExists(workbook)) {
            try (InputStream starter = openResource("/Veg.xlsx")) {
                Files.copy(starter, workbook);
            }
        }
        if (!Files.isRegularFile(workbook)) {
            throw new FileNotFoundException("Excel workbook not found: " + workbook);
        }

        String python = System.getenv("VEG_PYTHON");
        if (python == null || python.isBlank()) {
            python = System.getProperty("os.name").startsWith("Windows") ? "py" : "python3";
        }

        Path script = Files.createTempFile("veg-stock-", ".py");
        int exitCode;
        try {
            try (InputStream source = openResource("/Test.py")) {
                Files.copy(source, script, StandardCopyOption.REPLACE_EXISTING);
            }
            Process process = new ProcessBuilder(python, "-u", script.toString(), workbook.toString())
                    .inheritIO()
                    .start();
            try {
                exitCode = process.waitFor();
            } catch (InterruptedException interrupted) {
                process.destroyForcibly();
                throw interrupted;
            }
        } finally {
            Files.deleteIfExists(script);
        }

        if (exitCode != 0) {
            System.exit(exitCode);
        }
    }

    private static InputStream openResource(String name) throws FileNotFoundException {
        InputStream resource = PythonRunner.class.getResourceAsStream(name);
        if (resource == null) {
            throw new FileNotFoundException("Packaged resource not found: " + name);
        }
        return resource;
    }
}
