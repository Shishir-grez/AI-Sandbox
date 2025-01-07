import CodeMirror from '@uiw/react-codemirror';

function App() {
  return (
    <CodeMirror
      value="console.log('hello world!');"
      height="200px"
      basicSetup={{
        foldGutter: false,
        dropCursor: false,
        allowMultipleSelections: false,
        indentOnInput: false,
      }}
    />
  );
}
export default App;
