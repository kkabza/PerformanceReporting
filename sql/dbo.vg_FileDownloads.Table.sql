USE [Taxsale2024]
GO
/****** Object:  Table [dbo].[vg_FileDownloads]    Script Date: 3/31/2025 3:44:47 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[vg_FileDownloads](
	[FileID] [int] IDENTITY(1,1) NOT NULL,
	[FileName] [varchar](50) NULL,
	[UserID] [uniqueidentifier] NULL,
	[FileDate] [datetime] NULL
) ON [PRIMARY]
GO
