const path = require("path");
require("dotenv").config();
var express = require("express");
var router = express.Router();

const database = require("../database/database.js");

var db = new database();

// Enforce foreign key checks
db.get("PRAGMA foreign_keys = ON");

// This code sets up a GET endpoint on the router that will return all rows
// from the "todos" table in the database.

router.get("/", (req, res) => {
  // Execute a SQL query to select all rows from the "todos" table
  db.all("SELECT * FROM todos", (err, rows) => {
    if (err) {
      // If there was an error executing the SQL query, handle the error
      if (process.env.NODE_ENV != "development") {
        // In production, send the error to a Azure App Insights logging service
        global.client.trackException({ exception: err });
      } else {
        // In development, log the error to the console
        console.log(err);
      }

      // Send a 500 status code and error message back to the client
      return res.status(500).json({ error: err.message });
    }

    // If the query was successful, send the results back to the client
    res.json({ data: rows });
  });
});

// This code sets up a GET endpoint on the router that will return a specific
// row from the "todos" table in the database, based on the ID parameter passed in the URL.
router.get("/:id", (req, res) => {
  // Extract the ID parameter from the request URL
  const id = req.params.id;

  // Execute a SQL query to select a row from the "todos" table with the given ID
  db.get("SELECT * FROM todos WHERE id = ?", id, (err, row) => {
    if (err) {
      // If there was an error executing the SQL query, handle the error
      if (process.env.NODE_ENV != "development") {
        // In production, send the error to a Azure App Insights logging service
        global.client.trackException({ exception: err });
      } else {
        // In development, log the error to the console
        console.log(err);
      }

      // If there was an error executing the SQL query,
      // send a 500 status code and error message back to the client
      return res.status(500).json({ error: err.message });
    }

    if (!row) {
      // If no rows were returned by the SQL query, send a 404 status
      // code and "Todo not found" error message back to the client
      return res.status(404).json({ error: "Todo not found" });
    }

    // If the query was successful and a row was returned,
    // send the row data back to the client
    res.json({ data: row });
  });
});

// This code sets up a POST endpoint on the router that will
// add a new row to the "todos" table in the database.

router.post("/", (req, res) => {
  // Extract the request body data
  const { todo, priority, status, category, due_date } = req.body;

  // Execute a SQL query to insert a new row into the "todos" table with the given data
  db.run(
    `INSERT INTO todos (todo, priority, status, category, due_date) VALUES (?, ?, ?, ?, ?)`,
    [todo, priority, status, category, due_date],
    function (err) {
      if (err) {
        // If there was an error executing the SQL query, handle the error
        if (process.env.NODE_ENV != "development") {
          // In production, send the error to a Azure App Insights logging service
          global.client.trackException({ exception: err });
        } else {
          // In development, log the error to the console
          console.log(err);
        }

        // If there was an error executing the SQL query,
        // send a 500 status code and error message back to the client
        return res.status(500).json({ error: err.message });
      }

      // If the query was successful, send a 201 status code and
      // the newly created row data back to the client
      res.status(201).json({
        data: {
          id: this.lastID,
          todo,
          priority,
          status,
          category,
          due_date,
        },
      });
    }
  );
});

// This code sets up a DELETE endpoint on the router that will delete
// a row from the "todos" table in the database.

router.delete("/:id", async function (req, res) {
  // Extract the ID of the row to be deleted from the request parameters
  const id = req.params.id;

  // Define a SQL query to delete the row with the given ID from the "todos" table
  const query = "DELETE FROM todos WHERE id = ?";

  try {
    // Execute the SQL query using the "db" object and the ID extracted from the request parameters
    const result = await db.run(query, [id]);

    // If no rows were affected by the query, send a 404 status code and error message back to the client
    if (result.changes === 0) {
      return res.status(404).json({ error: "Todo not found" });
    }

    // If the query was successful and at least one row was affected, send a 200 status code and success message back to the client
    res.json({ message: "Todo deleted successfully" });
  } catch (err) {
    // If there was an error executing the SQL query, log the error to the console and send a 500 status code and error message back to the client
    console.log(err);
    return res.status(500).json({ error: err.message });
  }
});

router.put("/:id", function (req, res) {
    // Get the todo ID from the URL parameter
    const id = req.params.id;
    
    // Get the values for the update from the request body
    const { todo, priority, status, category, due_date } = req.body;
    
    // Check whether priority exists
    const qr = `SELECT * FROM priorities WHERE id = ?`;
    db.get(qr, [priority], function (err, row) {
        if (err) {
        // If there was an error executing the SQL query, handle the error
        if (process.env.NODE_ENV != "development") {
            // In production, send the error to a Azure App Insights logging service
            global.client.trackException({ exception: err });
        } else {
            // In development, log the error to the console
            console.log(err);
        }
    
        // If there was an error executing the SQL query,
        // send a 500 status code and error message back to the client
        return res.status(500).json({ error: err.message });
        }
    
        // Check whether Priority exists
        if (!row) {
        // Return a 404 error if the priority doesn't exist
        return res
            .status(404)
            .json({ error: "The priority provided does not exist!" });
        } else {
        // Update the todo in the database
        const query = `UPDATE todos SET todo = COALESCE(?, todo), priority = COALESCE(?, priority), status = COALESCE(?, status), category = COALESCE(?, category), due_date = COALESCE(?, due_date) WHERE id = ?`;
    
        db.run(
            query,
            [todo, priority, status, category, due_date, id],
            function (err) {
            if (err) {
                // Log and return an error if there is a problem with the update
                if (process.env.NODE_ENV != "development") {
                global.client.trackException({ exception: err });
                } else {
                console.log(err);
                }
                return res.status(500).json({ error: err.message });
            }
    
            if (this.changes === 0) {
                // Return a 404 error if no rows were affected by the update
                return res.status(404).json({ error: "Todo not found" });
            }
    
            // Return the updated todo
            res.json({
                data: {
                id: id,
                todo: todo || this.todo,
                priority: priority || this.priority,
                status: status || this.status,
                category: category || this.category,
                due_date: due_date || this.due_date,
                },
            });
            }
        );
        }
    });
    });

module.exports = router;