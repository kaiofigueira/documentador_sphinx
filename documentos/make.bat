@ECHO OFF
REM Entrar no diretório onde o script está localizado
pushd %~dp0

REM Define o comando do Sphinx se não estiver configurado
if "%SPHINXBUILD%" == "" (
    set SPHINXBUILD=sphinx-build
)

set SOURCEDIR=.
set BUILDDIR=_build

REM Testa se o comando sphinx-build está disponível
%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
    echo.
    echo O comando 'sphinx-build' não foi encontrado.
    echo Certifique-se de que o Sphinx está instalado.
    echo Você pode instalar com: pip install sphinx
    echo.
    echo Ou defina a variável SPHINXBUILD com o caminho completo do executável.
    exit /b 1
)

REM Se nenhum argumento foi passado, mostra ajuda
if "%1" == "" goto help

REM Roda o comando passado como argumento (ex: html, clean, etc)
%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
REM Mostra os comandos disponíveis do make do Sphinx
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
