import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.api import api_router

from src.core.modules.services import StaticAnalyzerService
from src.models.entities import ClassEntity

app = FastAPI()
app.include_router(api_router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    # uvicorn.run(
    #     'main:app',
    #     host='0.0.0.0',
    #     port=8000,
    # )

    code_text = """
using System;\n
using System.Linq;\n
using Strategies.SortStrategy;\n
using Strategies.SwapStrategy;\n
using Strategies.OrderStrategy;\n
\n
namespace UserMatrix;\n
\n
public class Matrix {\n
    private double[][] _data;\n
\n
    public int Rows => _data.Length;\n
    public int Columns => Rows == 0 ? 0 : _data.Select(row => row.Length).Max();\n
\n
    public double this[int i, int j] => _data[i][j];\n
\n
    public Matrix() => _data = new double[0][] {};\n
\n
    public Matrix(int size) => GetEmpty(size);\n
\n
    public Matrix(int rows, int columns) => GetEmpty(rows, columns);\n
\n
    public Matrix(double[][] initData) => _data = initData;\n
\n
    public Matrix(double[,] initData) {\n
        int rows = initData.GetLength(0);\n
        int columns = initData.GetLength(1);\n
\n
        _data = new double[rows][];\n
        for (int i = 0; i < rows; ++i) {\n
            _data[i] = new double[columns];\n
            for (int j = 0; j < columns; ++j) {\n
                _data[i][j] = initData[i, j];\n
            }\n
        }\n
    }\n
\n
    public static Matrix GetEmpty(int size) => GetEmpty(size, size);\n
\n
    public static Matrix GetEmpty(int rows, int columns) {\n
        rows = Math.Max(rows, 0);\n
        columns = Math.Max(columns, 0);\n
\n
        double[][] initData = new double[rows][].Select(row => row = new double[columns].Select(item => item = 0).ToArray()).ToArray();\n
        return new Matrix(initData);\n
    }\n
\n
}
    """

    csharp_lines = [
        """
public class SimpleClass
{
    private int number = 123;
    public string name;
    
    public void SetNumber(int value)
    {
        number = value;
    }
    
    public int GetNumber()
    {
        return number;
    }
}
        """,
        """
internal sealed class SealedClass
{
    public double Balance { get; set; }
    
    internal string ProcessData(string input)
    {
        return input.ToUpper();
    }
}
        """,
        """
abstract class AbstractClass
{
    protected float percentage;
    
    public abstract void Calculate();
}
        """,
        """
public class GenericClass<T>
{
    private T data;
    
    public void SetData(T newData)
    {
        data = newData;
    }
    
    public T GetData()
    {
        return data;
    }
}
        """,
        """
public class DerivedClass : BaseClass, ISomeInterface
{
    public override void MethodFromBase()
    {
        // Method implementation
    }
    
    public void MethodFromInterface()
    {
        // Interface method implementation
    }
}
        """,
        """
partial class PartialClass
{
    public int PartOneMethod()
    {
        return 1;
    }
}
        """
    ]

    # entities = [ClassEntity(line) for line in csharp_lines]
    # print(entities)

    code = StaticAnalyzerService.add_xml_documentation(code_text)
    print(code)
